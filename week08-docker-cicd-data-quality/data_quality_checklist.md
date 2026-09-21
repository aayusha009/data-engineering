# Data Quality Checklist

- [x] Row count check — fails if the result set is unexpectedly empty
- [x] Not-null check — order_id, status
- [x] Uniqueness check — order_id
- [x] Accepted values check — status must be one of: pending, shipped, delivered, cancelled
- [x] Freshness check — orders source, warn after 12h, error after 24h
- [ ] Anomaly check (day-over-day swing) — not implemented yet
