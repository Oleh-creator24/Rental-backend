from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from users.models import User
from listings.models import Listing
from bookings.models import Booking
from reviews.models import Review
import json


class CustomAdminSite(admin.AdminSite):
    site_header = "Система аренды жилья"
    site_title = "Панель управления"
    index_title = "Добро пожаловать в админ-панель"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("analytics/", self.admin_view(self.analytics_view), name="analytics"),
        ]
        return custom_urls + urls

    def analytics_view(self, request):
        # --- Основная статистика ---
        total_users = User.objects.count()
        total_listings = Listing.objects.count()
        total_bookings = Booking.objects.count()
        total_reviews = Review.objects.count()
        active_listings = Listing.objects.filter(is_available=True).count()

        # --- Топ объявления и владельцы ---
        top_listings = Listing.objects.order_by("-view_count")[:3]
        top_owners = (
            User.objects.filter(listings__isnull=False)
            .annotate(total=Count("listings"))
            .order_by("-total")[:3]
        )

        # --- 📊 Бронирования по месяцам ---
        monthly_bookings = (
            Booking.objects.annotate(month=TruncMonth("start_date"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )
        monthly_bookings_dict = {
            b["month"].strftime("%b %Y"): b["total"] for b in monthly_bookings if b["month"]
        }

        # --- 🏙️ Объявления по городам (топ-5) ---
        listings_by_city = (
            Listing.objects.values("city__name")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )
        listings_by_city_dict = {
            item["city__name"] or "Не указан": item["total"] for item in listings_by_city
        }

        # ---  Пользователи по ролям ---
        users_by_role = {
            "Администраторы": User.objects.filter(is_staff=True, is_superuser=False).count(),
            "Пользователи": User.objects.filter(is_staff=False, is_superuser=False).count(),
            "Суперпользователи": User.objects.filter(is_superuser=True).count(),
        }

        # ---  Бронирования по статусу ---
        bookings_by_status = (
            Booking.objects.values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )
        bookings_by_status_dict = {b["status"]: b["total"] for b in bookings_by_status}

        # --- Подготовка JSON для Chart.js ---
        analytics_data = {
            "users_by_role": users_by_role,
            "listings_by_city": listings_by_city_dict,
            "bookings_by_status": bookings_by_status_dict,
            "monthly_bookings": monthly_bookings_dict,
        }

        context = dict(
            self.each_context(request),
            total_users=total_users,
            total_listings=total_listings,
            total_bookings=total_bookings,
            total_reviews=total_reviews,
            active_listings=active_listings,
            top_listings=top_listings,
            top_owners=top_owners,
            title="Аналитика системы аренды жилья",
            analytics_json=json.dumps(analytics_data, ensure_ascii=False),
        )

        return TemplateResponse(request, "admin/analytics.html", context)


custom_admin_site = CustomAdminSite(name="custom_admin")
