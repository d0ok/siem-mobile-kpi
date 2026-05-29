# SIEM KPI 4G/5G — Supervision Intelligente des Réseaux Mobiles

> Projet Académique — Ingénierie des Réseaux Mobiles

## Description
Plateforme de supervision temps réel des KPI télécom (RSRP, RSRQ, RSCP, Ec/N0) avec détection d'anomalies via Wazuh SIEM et Isolation Forest ML.

## Stack technologique
- **Wazuh** — SIEM et détection d'anomalies
- **Elasticsearch** — Stockage et indexation
- **Kibana** — Dashboard temps réel
- **Filebeat** — Collecte de logs
- **Python** — Génération de logs + ML (Isolation Forest)
- **Docker Compose** — Orchestration

## Démarrage rapide
\`\`\`bash
# Prérequis
sudo sysctl -w vm.max_map_count=262144

# Lancer le stack complet
docker-compose up -d

# Vérifier
docker-compose ps
curl http://localhost:9200/_cat/indices?v
\`\`\`

## Accès
| Service | URL |
|---------|-----|
| Kibana Dashboard | http://localhost:5601 |
| Elasticsearch API | http://localhost:9200 |
| Wazuh API | http://localhost:55000 |

## Règles SIEM
| Rule ID | Level | Description |
|---------|-------|-------------|
| 100001 | 12 | RSRP critique < -100 dBm (LTE) |
| 100002 | 7 | RSRP dégradé WARNING (LTE) |
| 100003 | 12 | RSCP critique < -95 dBm (UMTS) |
| 100004 | 14 | Anomalie ML détectée |
| 100005 | 15 | Brouillage potentiel (5 chutes/60s) |

## Dataset
- DT1 : LTE 4G — 10 428 mesures terrain (RSRP, RSRQ, Band 3/20)
- DT2/DT3 : UMTS 3G — 8 332 mesures terrain (RSCP, Ec/N0, Band 8)
