# مرجع API

يوفر CryptoHub واجهتي API خلفيتين: **Go API** (البوابة الرئيسية) و**Python API** (محرك الذكاء الاصطناعي والتحليل الكمي).

## عناوين URL الأساسية

| الخدمة | الرابط | البادئة |
|--------|--------|---------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

## نقاط نهاية Python API

### فحص الحالة

```
GET /health
```

### تحليل الذكاء الاصطناعي

#### تحليل بث AI (SSE)

```
POST /api/v1/ai/analyze
```

| الحقل | النوع | الوصف |
|-------|-------|-------|
| `symbol` | string | رمز التداول (مثل `BTC/USDT`) |
| `analysis_type` | string | `comprehensive`، `technical`، `fundamental` |
| `timeframe` | string | `1D`، `4H`، `1H` إلخ |

#### الحصول على نتيجة التحليل

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### تحليل متعدد العوامل سريع

```
POST /api/v1/ai/fast-analyze
```

### الاختبار الخلفي

#### تشغيل اختبار خلفي

```
POST /api/v1/backtest/run
```

| الحقل | النوع | الافتراضي | الوصف |
|-------|-------|-----------|-------|
| `strategy_id` | string | مطلوب | معرف الاستراتيجية |
| `symbol` | string | مطلوب | زوج التداول |
| `timeframe` | string | `1H` | الإطار الزمني |
| `start_date` | string | مطلوب | تاريخ ISO |
| `end_date` | string | مطلوب | تاريخ ISO |
| `initial_capital` | number | `10000` | رأس المال الأولي |

#### الحصول على النتيجة

```
GET /api/v1/backtest/{backtest_id}
```

#### الحصول على التقرير

```
GET /api/v1/backtest/{backtest_id}/report
```

### محرك الاستراتيجيات

```
POST /api/v1/strategy/compile
POST /api/v1/strategy/start
POST /api/v1/strategy/stop/{strategy_id}
GET  /api/v1/strategy/{strategy_id}/status
```

### المؤشرات

```
POST /api/v1/indicator/calculate
GET  /api/v1/indicator/list
```

### توليد الكود

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## المصادقة

تتطلب نقاط النهاية المحمية رمز Bearer في ترويسة `Authorization`:

```
Authorization: Bearer <jwt_token>
```

## استجابات الأخطاء

```json
{ "code": 400, "message": "فشل التحقق", "detail": "الحقل 'symbol' مطلوب" }
```
