# 🌦️ Weather Data Dashboard for Poland 🇵🇱 (IMGW API + PostgreSQL + Power BI)

A complete data pipeline project that collects current weather data from IMGW's public API, processes and stores it in a PostgreSQL database, and visualizes it using Power BI. The goal is also to learn and apply data engineering tools such as Apache Airflow.

---

## 📌 Project Overview

This project demonstrates how to:
- Extract current weather data from the IMGW API
- Transform and clean the data using Python
- Store the data in a PostgreSQL database
- Schedule regular updates using Apache Airflow
- Visualize weather conditions across Poland using Power BI

---

## 🧱 Architecture

```plaintext
[IMGW API] → [Python ETL Script] → [PostgreSQL] → [Power BI Dashboard]
                               ↘
                            [Airflow (DAG)]