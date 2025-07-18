
# `axios` vs `fetch`
---

### ⚔️ `axios` vs `fetch` (so sánh nhanh)

* 🧩 **Cài đặt**:

  * `fetch`: Có sẵn
  * `axios`: Phải `npm install`

* 🧠 **Xử lý JSON**:

  * `fetch`: Phải `.json()` thủ công
  * `axios`: Có sẵn `res.data`

* ❗ **Bắt lỗi HTTP**:

  * `fetch`: Không tự bắt lỗi status ≠ 200
  * `axios`: Tự động bắt lỗi

* 🧾 **Gửi JSON**:

  * `fetch`: Phải `JSON.stringify`
  * `axios`: Tự làm

* ⛔ **Hủy request**:

  * `fetch`: Khó
  * `axios`: Có `CancelToken`

---

✅ **Kết luận**:

* `fetch` đơn giản, nhẹ → phù hợp dự án nhỏ.
* `axios` mạnh, tiện → phù hợp dự án lớn.
