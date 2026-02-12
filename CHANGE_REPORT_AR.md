# تقرير التعديلات (للدعم السريع)

هذا التقرير يوضح **ما الذي تم تغييره** في مشروع بوابة الهوتسبوت، مع ذكر **الملف + السطر** لتسهيل التشخيص السريع عند حدوث أي مشكلة.

---

## 1) آخر تعديلات منفذة (مرتبة حسب الأهمية)

### A) جعل صفحة الدخول بيوزر فقط فعليًا

1. **تأكيد نمط تسجيل الدخول من الإعدادات**
   - الملف: `hotspot DARAK/config/config.js`
   - السطر: `4`
   - التغيير: ضبط `"login-type": "username"`.

2. **تسجيل الدخول اليدوي يرسل username فقط**
   - الملف: `hotspot DARAK/js/main.min.js`
   - السطر: `34`
   - التغيير: الدالة `userLogin()` تبني الرابط بهذا الشكل:
     - `/login?username=...&var=callBack`
   - ملاحظة: لا يتم تمرير `password` في الطلب.

3. **تسجيل الدخول التلقائي من الكوكيز يرسل username فقط**
   - الملف: `hotspot DARAK/js/hotCookie.min.js`
   - السطر: `4`
   - التغيير: الدالة `cookieLogin()` ترسل:
     - `/login?username=...&var=callBack`
   - ملاحظة: لا يتم إلحاق `password` في طلب تسجيل الدخول التلقائي.

4. **تحديث رسالة الخطأ لتناسب وضع اليوزر فقط**
   - الملف: `hotspot DARAK/js/main.min.js`
   - السطر: `23`
   - التغيير: رسالة `invalid username or password|not found` أصبحت موجّهة لخطأ اسم المستخدم.

---

### B) حذف حقل كلمة السر من HTML (كما طلبت)

1. **إزالة بلوك كلمة السر بالكامل من نموذج الدخول**
   - الملف: `hotspot DARAK/index.html`
   - النطاق الحالي المتأثر في النموذج: من السطر `47` إلى `75`.
   - النتيجة: النموذج يحتوي الآن على:
     - حقل اسم المستخدم فقط (`username-field`).
     - بدون `<input name="password">` داخل الصفحة.

---

## 2) نقاط مهمة جدًا قبل أي تعديل مستقبلي

1. ملف `templates.min.js` ما زال يحتوي منطق وضع `both` (يوزر + كلمة سر):
   - الملف: `hotspot DARAK/js/templates.min.js`
   - الأسطر: `7` إلى `19`
   - السبب: هذا منطق عام للقالب بحسب `login-type`.
   - الوضع الحالي آمن لأن `login-type` مضبوط على `username` في الإعدادات.

2. ملف `hotCookie.min.js` ما زال يدعم تخزين كلمة السر في الكوكيز داخليًا كمنطق عام:
   - الملف: `hotspot DARAK/js/hotCookie.min.js`
   - الأسطر: `2` إلى `4`
   - المهم: تدفق الدخول الفعلي الحالي لا يرسل `password` في طلب `/login`.

---

## 3) كيف تتحقق بسرعة إذا حصلت مشكلة

### فحص أن الصفحة ما فيها password field
```bash
rg -n 'name="password"|password-field' 'hotspot DARAK/index.html'
```
المتوقع: لا نتائج لحقل كلمة السر داخل `index.html`.

### فحص أن الدخول يرسل username فقط
```bash
rg -n 'function userLogin|/login\?username=' 'hotspot DARAK/js/main.min.js' 'hotspot DARAK/js/hotCookie.min.js'
```
المتوقع: ظهور `/login?username=...&var=callBack` فقط.

### فحص نمط الدخول من الإعدادات
```bash
rg -n '"login-type"' 'hotspot DARAK/config/config.js'
```
المتوقع: القيمة `username`.

---

## 4) مرجع سريع للتراجع (Rollback)

إذا أردت الرجوع قبل آخر تعديل (حذف حقل كلمة السر من HTML):

```bash
git log --oneline -n 5
git revert <commit_hash>
```

> استخدم `revert` بدل `reset` إذا كنت لا تريد كسر تاريخ المشروع.

---

## 5) ملخص تنفيذي

- تم توحيد السلوك على **اسم المستخدم فقط** (Config + JS + UI).
- تم حذف حقل كلمة السر من الواجهة فعليًا.
- هذا الملف (`CHANGE_REPORT_AR.md`) مخصص لك كمرجع صيانة سريع عند أي خطأ مستقبلي.
