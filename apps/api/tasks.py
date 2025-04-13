# api/tasks.py

from celery import shared_task
from django_redis import get_redis_connection
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

@shared_task
def increment_url_visit(short_code):
    """
    Belirli bir kısa URL'nin ziyaret sayısını arttırır.
    Önce Redis'te sayacı arttırır, sonra belirli aralıklarla veritabanını günceller.
    """
    try:
        # Redis bağlantısı al
        redis_conn = get_redis_connection("default")
        
        # Redis'te ziyaret sayısını arttır
        redis_key = f"url_visits:{short_code}"
        redis_conn.incr(redis_key)
        
        # Belirli aralıklarla veritabanını güncelle
        # Eğer Redis'teki değer belirli bir eşiği aşarsa veya
        # Belirli bir süre geçtiyse veritabanını güncelle
        if redis_conn.get(f"update_lock:{short_code}") is None:
            # Güncelleme kilidi oluştur (30 saniyelik)
            redis_conn.setex(f"update_lock:{short_code}", 30, 1)
            
            # Redis'teki değeri al ve veritabanını güncelle
            visits = int(redis_conn.get(redis_key) or 0)
            update_db_visits.delay(short_code, visits)
        
        return True
    except Exception as e:
        logger.error(f"increment_url_visit error: {str(e)}")
        return False

@shared_task
def update_db_visits(short_code, visits):
    """
    Veritabanındaki ziyaret sayısını günceller
    """
    try:
        # Modeli dinamik olarak içe aktar
        ShortURL = apps.get_model('api', 'ShortURL')
        
        try:
            url_obj = ShortURL.objects.get(short_code=short_code)
            url_obj.visits = visits
            url_obj.save(update_fields=['visits'])
            
            # Başarılı güncelleme sonrası Redis'i sıfırlama opsiyonel
            # redis_conn = get_redis_connection("default")
            # redis_conn.delete(f"url_visits:{short_code}")
            
            return True
        except ShortURL.DoesNotExist:
            logger.warning(f"ShortURL not found: {short_code}")
            return False
    except Exception as e:
        logger.error(f"update_db_visits error: {str(e)}")
        return False

@shared_task
def sync_all_visit_counts():
    """
    Tüm URL'lerin ziyaret sayılarını Redis'ten veritabanına senkronize eder.
    Zamanlı bir görev olarak çalıştırılabilir.
    """
    try:
        # Modeli dinamik olarak içe aktar
        ShortURL = apps.get_model('api', 'ShortURL')
        
        redis_conn = get_redis_connection("default")
        
        # Redis'teki tüm URL ziyaret anahtarlarını bul
        visit_keys = redis_conn.keys("url_visits:*")
        updated_count = 0
        
        for key in visit_keys:
            short_code = key.decode().split(":")[-1]
            visits = int(redis_conn.get(key) or 0)
            
            try:
                url_obj = ShortURL.objects.get(short_code=short_code)
                url_obj.visits = visits
                url_obj.save(update_fields=['visits'])
                
                # Başarılı güncelleme sonrası Redis'i sıfırla
                redis_conn.delete(key)
                updated_count += 1
            except ShortURL.DoesNotExist:
                continue
        
        return {'updated': updated_count, 'total': len(visit_keys)}
    except Exception as e:
        logger.error(f"sync_all_visit_counts error: {str(e)}")
        return False

@shared_task
def cleanup_expired_locks():
    """
    Süresi dolmuş olabilecek kilitleri temizler
    """
    try:
        redis_conn = get_redis_connection("default")
        lock_keys = redis_conn.keys("update_lock:*")
        
        for key in lock_keys:
            # Kilitlerin süresini kontrol et ve gerektiğinde temizle
            if redis_conn.ttl(key) < 0:
                redis_conn.delete(key)
        
        return {'cleaned_locks': len(lock_keys)}
    except Exception as e:
        logger.error(f"cleanup_expired_locks error: {str(e)}")
        return False