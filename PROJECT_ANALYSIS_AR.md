# تحليل مشروع Wifi-network-is-

## نظرة عامة
هذا المشروع عبارة عن **بوابة تسجيل دخول Hotspot** (غالبًا لبيئة MikroTik) مكتوبة بصفحات HTML/CSS/JavaScript ثابتة، ومُهيأة بالكامل للغة العربية وتجربة استخدام RTL.

الواجهة الرئيسية موجودة في:
- `hotspot DARAK/index.html`

وتعتمد على:
- `js/init.min.js` لقراءة الإعدادات وحقنها في الصفحة.
- `config/config.js` لضبط اسم الشبكة، الأسعار، نقاط البيع، وسياسات الإدخال والحظر.
- `js/main.min.js` لمعالجة تسجيل الدخول/الخروج، الاستعلام الدوري عن الحالة، ورسائل الأخطاء.

## بنية المشروع
- `hotspot DARAK/index.html`: صفحة الدخول الرئيسية وتحتوي أقسام: تسجيل الدخول، الأسعار، نقاط البيع، الحالة، الحظر، والخدمات.
- `hotspot DARAK/login.html`, `status.html`, `logout.html`, `alogin.html`, `redirect.html`: صفحات مرتبطة بتدفق الـ hotspot.
- `hotspot DARAK/config/config.js`: ملف الإعدادات المركزي.
- `hotspot DARAK/js/*.min.js`: المنطق التشغيلي (مضغوط/مُصغّر).
- `hotspot DARAK/css/style.min.css`: التنسيق العام.
- `hotspot DARAK/fonts/*` و`hotspot DARAK/img/*`: الأصول البصرية.

## كيف يعمل النظام (تدفق مبسّط)
1. عند تحميل الصفحة، `init.min.js` يحمّل `config/config.js`.
2. القيم من `hotspotConfig` تُحقن داخل العناصر التي تحمل خصائص `data-*` مثل:
   - `data-network-name`
   - `data-service-number`
   - `data-price-button`
3. عند الضغط على زر تسجيل الدخول، `main.min.js` يرسل طلبًا:
   - `/login?username=...&password=...&var=callBack`
4. بعد نجاح الدخول يبدأ استعلام دوري كل ثانية:
   - `/status?var=callBack`
5. عند الخروج يرسل:
   - `/logout?var=callBack`

## أبرز الإعدادات في config.js
- معلومات الهوية:
  - `network-name`
  - `service-number`
  - `news-line`
- إعدادات الإدخال:
  - `input-to-arabic-numbers`
  - `input-rm-white-spaces`
  - `input-only-numbers` ...إلخ
- التحكم في الحظر:
  - `enable-hot-blocker`
  - `try-count`
  - `warn-when`
  - `block-time`
- التخصيص التجاري:
  - `profiles` (الأسعار والباقات)
  - `sell-points` (نقاط البيع)
  - `loan-text`

## ملاحظات تقنية مهمة
- الشيفرة التشغيلية الأساسية مضغوطة (`*.min.js`)، ما يصعّب الصيانة والتعديل المباشر.
- توجد قيم واجهة كثيرة مبنية على الاستبدال النصي `{{...}}` وخصائص `data-*`.
- يوجد قسم Swiper/إعلانات في `main.min.js` يفترض وجود عناصر معينة (مثل `swiper-slide`)؛ أي نقص في DOM قد يؤدي لأخطاء وقت التشغيل.
- يوجد تكرار لمعرّف `id="loan"` في `index.html` (المعرّف يجب أن يكون فريدًا في الصفحة).

## توصيات لتحسين المشروع
1. الاحتفاظ بنسخة غير مضغوطة من JavaScript (source) لتسهيل الصيانة.
2. إضافة `README` يوثق:
   - طريقة النشر على MikroTik
   - طريقة تعديل `config/config.js`
   - تفسير كل خيار إعداد
3. إصلاح تكرار المعرّفات في `index.html`.
4. إضافة فحوصات أساسية (Lint) على HTML/JS قبل النشر.
5. فصل منطق الأعمال عن DOM بشكل أوضح لتسهيل التطوير المستقبلي.

## الخلاصة
المشروع جاهز تشغيليًا كبوابة Hotspot عربية وقابل للتخصيص بدرجة جيدة عبر ملف إعدادات واحد. نقطة الضعف الأساسية حاليًا هي قابلية الصيانة بسبب الاعتماد على ملفات JavaScript مضغوطة فقط، مع حاجة إلى تحسينات تنظيمية بسيطة (توثيق + تنظيف DOM).
