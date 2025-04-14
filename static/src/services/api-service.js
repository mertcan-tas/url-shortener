import client from "../client";

class UserService {
  login(payload) {
    return client.post("authentication/login/", payload);
  }

  register(payload) {
    return client.post("authentication/register/", payload);
  }

  userDetail() {
    return client.get("authentication/user/");
  }
}

export default new UserService();
