from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from rest_framework import views, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_redis import get_redis_connection
from .models import ShortURL
from .serializers import ShortURLSerializer
from .tasks import increment_url_visit
from rest_framework.permissions import AllowAny

User = get_user_model()

# URL Oluşturma View
class CreateShortURLView(generics.CreateAPIView):
    serializer_class = ShortURLSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

# URL Listeleme View
class ListShortURLsView(generics.ListAPIView):
    """
    Tüm kısa URL'leri listeler.
    ?my=true parametresi ile kullanıcının kendi URL'leri filtrelenebilir.
    """
    serializer_class = ShortURLSerializer
    
    def get_queryset(self):
        queryset = ShortURL.objects.all().order_by('-created_at')
        
        # URL parametresi olarak 'my' gönderilmişse ve kullanıcı oturum açmışsa
        # sadece kullanıcının kendi URL'lerini göster
        if self.request.query_params.get('my') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset

# Kullanıcının Kendi URL'lerini Listeleme View
class MyShortURLsView(generics.ListAPIView):
    """
    Oturum açmış kullanıcının kendi URL'lerini listeler.
    Kimlik doğrulaması gerektirir.
    """
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user).order_by('-created_at')

# Detaylı URL Görüntüleme View
class ShortURLDetailView(generics.RetrieveAPIView):
    """
    Belirli bir kısa URL'nin detaylarını görüntüler.
    """
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'id'

# URL Güncelleme View
class UpdateShortURLView(generics.UpdateAPIView):
    """
    Mevcut bir URL'yi günceller.
    Sadece URL'nin sahibi olan kullanıcı güncelleyebilir.
    """
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

# URL Silme View
class DeleteShortURLView(generics.DestroyAPIView):
    """
    Bir URL'yi siler.
    Sadece URL'nin sahibi olan kullanıcı silebilir.
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

# Yönlendirme View (Kısa URL'yi Kullanarak)
@api_view(['GET'])
def redirect_to_original(request, short_code):
    """
    Kısa URL'den orijinal URL'ye yönlendirme yapar.
    Ziyaret sayısını asenkron olarak arttırır.
    """
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    
    # Ziyaret sayısını asenkron olarak arttır
    increment_url_visit.delay(short_code)
    
    return HttpResponseRedirect(short_url.original_url)

# Tüm URL'ler İçin İstatistikler View
class URLStatsView(generics.ListAPIView):
    """
    Tüm URL'lerin istatistiklerini gösterir.
    Redis'teki gerçek zamanlı sayaçları da içerir.
    """
    serializer_class = ShortURLSerializer
    
    def get_queryset(self):
        return ShortURL.objects.all().order_by('-visits')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Redis'teki gerçek zamanlı sayaçları da ekle
        redis_conn = get_redis_connection("default")
        data = serializer.data
        
        for item in data:
            short_code = item['short_code']
            redis_key = f"url_visits:{short_code}"
            redis_visits = redis_conn.get(redis_key)
            
            if redis_visits:
                item['real_time_visits'] = int(redis_visits) + item['visits']
            else:
                item['real_time_visits'] = item['visits']
        
        return Response(data)

# Belirli URL İçin İstatistikler View
class URLDetailStatsView(generics.RetrieveAPIView):
    """
    Belirli bir URL'nin istatistiklerini gösterir.
    Redis'teki gerçek zamanlı sayacı da içerir.
    """
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Redis'teki gerçek zamanlı sayacı da ekle
        redis_conn = get_redis_connection("default")
        redis_key = f"url_visits:{instance.short_code}"
        redis_visits = redis_conn.get(redis_key)
        
        if redis_visits:
            data['real_time_visits'] = int(redis_visits) + instance.visits
        else:
            data['real_time_visits'] = instance.visits
        
        return Response(data)


# İstatistik Dashboard View
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    Oturum açmış kullanıcı için dashboard istatistiklerini döndürür.
    - Toplam URL sayısı
    - Toplam ziyaret sayısı
    - En popüler URL'ler
    """
    user_urls = ShortURL.objects.filter(user=request.user)
    total_urls = user_urls.count()
    
    # Veritabanından toplam ziyaret sayısı
    total_visits_db = sum(url.visits for url in user_urls)
    
    # Redis'den gerçek zamanlı ziyaret sayıları
    redis_conn = get_redis_connection("default")
    redis_visits = 0
    
    for url in user_urls:
        redis_key = f"url_visits:{url.short_code}"
        visits = redis_conn.get(redis_key)
        if visits:
            redis_visits += int(visits)
    
    total_visits = total_visits_db + redis_visits
    
    # En popüler 5 URL'yi al
    popular_urls = user_urls.order_by('-visits')[:5]
    popular_serializer = ShortURLSerializer(popular_urls, many=True, context={'request': request})
    
    # Popüler URL'lere Redis ziyaretlerini ekle
    popular_data = popular_serializer.data
    for item in popular_data:
        redis_key = f"url_visits:{item['short_code']}"
        redis_visits = redis_conn.get(redis_key)
        
        if redis_visits:
            item['real_time_visits'] = int(redis_visits) + item['visits']
        else:
            item['real_time_visits'] = item['visits']
    
    return Response({
        'total_urls': total_urls,
        'total_visits': total_visits,
        'popular_urls': popular_data
    })

# Sağlık Kontrolü View
@api_view(['GET'])
def health_check(request):
    """
    API servisinin çalışıp çalışmadığını kontrol etmek için.
    """
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)