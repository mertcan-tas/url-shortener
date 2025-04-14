import client from "../client";

class ShortenService {
  createShortenUrl(payload) {
    return client.post("urls/create/", payload);
  }

  getUserUrls() {
    return client.get("urls/my/");
  }

  deleteUrl(id) {
    return client.delete(`urls/${id}/delete/`);
  }
}

export default new ShortenService();