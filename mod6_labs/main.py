# main.py
"""Weather Application using Flet v0.28.3"""

import flet as ft
from weather_service import WeatherService
from config import Config
import json
from pathlib import Path
import asyncio
from datetime import datetime
from collections import defaultdict
import httpx

class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()

        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        
        # State Variables
        self.is_celsius = True 
        self.is_dark_mode = False 
        self.current_weather_data = None
        self.current_condition_main = "Clear" 
        self.forecast_text_controls = [] 
        
        # Animations
        self.theme_animation = ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
        self.text_animation = ft.Animation(300, ft.AnimationCurve.EASE_IN)
        self.pop_animation = ft.Animation(
            duration=500, 
            curve=ft.AnimationCurve.EASE_OUT_BACK 
        )
        self.error_animation = ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC)
        
        # Weather Data Storage
        self.daily_high_c = None
        self.daily_low_c = None
        
        # Theme Management Lists
        self.card_containers = [] 
        self.text_elements = []
        
        # UI Styles
        self.card_shadow = ft.BoxShadow(
            blur_radius=10,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
        
        # Geolocator
        self.geolocator = ft.Geolocator(
            on_error=self.on_gps_error
        )
        self.page.overlay.append(self.geolocator)
        
        self.setup_page()
        self.build_ui()
    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.animate_bgcolor = self.theme_animation
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        self.page.padding = 0
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()
    
    # --- Refactored UI Building Methods ---
    
    def _build_header(self):
        """Initialize title and settings menu."""
        self.title_icon = ft.Icon(ft.Icons.CLOUD, size=48, color=ft.Colors.BLUE_700)
        self.title = ft.Text(
            "Weather App", size=24, weight=ft.FontWeight.BOLD,
            font_family="Montserrat", color=ft.Colors.BLUE_700
        )
        
        self.unit_menu_item = ft.PopupMenuItem(
            text="Switch to °F", 
            icon=ft.Icons.THERMOSTAT, 
            on_click=self.toggle_unit
        )
        
        self.theme_menu_item = ft.PopupMenuItem(
            text="Dark Mode", 
            icon=ft.Icons.DARK_MODE, 
            on_click=self.toggle_theme
        )

        self.settings_button = ft.PopupMenuButton(
            icon=ft.Icons.MORE_VERT,
            tooltip="Settings",
            items=[self.unit_menu_item, self.theme_menu_item]
        )
        
        return ft.Row(
            [
                ft.Row([self.title_icon, self.title], alignment=ft.MainAxisAlignment.START, spacing=8, expand=True),
                self.settings_button 
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_search_controls(self):
        """Initialize search bar and action buttons."""
        self.city_input = ft.SearchBar(
            width=285, height=40,
            bar_shape=ft.RoundedRectangleBorder(radius=12),
            bar_elevation=1,
            bar_hint_text="Enter city name...",
            
            view_elevation=4,
            view_bgcolor=ft.Colors.WHITE if not self.is_dark_mode else "#1E1E1E",
            view_shape=ft.RoundedRectangleBorder(radius=10),
            
            on_submit=self.on_city_submit,
            on_tap=self.on_city_tap,
            controls=[], 
            expand=True,
        )
        
        self.refresh_searchbar_controls()
        self.city_input.bar_leading = ft.Icon(ft.Icons.APARTMENT, size=24, offset=ft.Offset(0.1, 0))
        self.city_input.bar_padding = ft.Padding(16, 0, 8, 0)
        
        self.search_icon = ft.Icon(ft.Icons.SEARCH, size=24, color=ft.Colors.BLUE_700)
        self.search_button = ft.Container(
            width=49, height=40, 
            bgcolor=ft.Colors.BLUE_50, 
            border_radius=8,
            alignment=ft.alignment.center, 
            content=self.search_icon,
            on_click=self.on_search,
            animate=self.theme_animation,
        )

        self.gps_icon = ft.Icon(ft.Icons.MY_LOCATION, size=24, color=ft.Colors.BLUE_700)
        self.gps_button = ft.Container(
            width=49, height=40, 
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
            alignment=ft.alignment.center, 
            content=self.gps_icon,
            on_click=self.on_gps_click, 
            animate=self.theme_animation,
            tooltip="Use Current Location"
        )
        
        return ft.Row(
            [self.city_input, self.search_button, self.gps_button], 
            alignment=ft.MainAxisAlignment.CENTER, 
            spacing=11
        )

    def _build_current_weather_display(self):
        """Initialize current weather cards and text."""
        # Weather Display Container 
        self.weather_container = ft.Container(
            visible=False, 
            border_radius=10,
            padding=8, width=345, 
            bgcolor=ft.Colors.BLUE_50,
            animate_scale=self.pop_animation,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN),
            scale=0.9,  
            opacity=0,  
        )

        # Text Elements
        self.main_temp_text = ft.Text("", size=48, weight=ft.FontWeight.BOLD, font_family="Montserrat", color=ft.Colors.WHITE)
        self.feels_like_text = ft.Text("", size=12, weight=ft.FontWeight.W_500, italic=True, font_family="Montserrat", color=ft.Colors.WHITE)
        self.desc_text = ft.Text("", size=12, weight=ft.FontWeight.W_600, italic=True, font_family="Montserrat", color=ft.Colors.WHITE)
        self.location_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD, font_family="Montserrat", color=ft.Colors.WHITE)
        
        self.high_low_text = ft.Text(
            "", 
            size=12, 
            weight=ft.FontWeight.W_600, 
            font_family="Montserrat", 
            color=ft.Colors.WHITE,
            animate_opacity=300,
        )

        # Metric Texts
        self.humidity_value_text = self.create_themed_text("--%", size=16, weight=ft.FontWeight.W_800)
        self.wind_value_text = self.create_themed_text("-- m/s", size=16, weight=ft.FontWeight.W_800)
        self.pressure_value_text = self.create_themed_text("-- hPa", size=16, weight=ft.FontWeight.W_800)
        self.cloud_value_text = self.create_themed_text("--%", size=16, weight=ft.FontWeight.W_800)
        
        # Metric Cards
        self.humidity_card = self.create_metric_card(
            ft.Icons.WATER_DROP, "Humidity", self.humidity_value_text, ft.Colors.BLUE
        )
        self.wind_card = self.create_metric_card(
            ft.Icons.AIR, "Wind Speed", self.wind_value_text, ft.Colors.CYAN
        )
        self.pressure_card = self.create_metric_card(
            ft.Icons.COMPRESS, "Pressure", self.pressure_value_text, ft.Colors.DEEP_ORANGE
        )
        self.cloud_card = self.create_metric_card(
            ft.Icons.CLOUD, "Cloudiness", self.cloud_value_text, ft.Colors.BLUE_GREY
        )
        
        self.humidity_wind_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row([self.humidity_card, self.wind_card], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.pressure_card, self.cloud_card], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=8,
            ),
            visible=False,
            animate_scale=self.pop_animation,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN),
            scale=0.9,
            opacity=0,
        )

    def _build_forecast_display(self):
        """Initialize forecast section."""
        self.forecast_row = ft.Row(
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[] 
        )
        
        self.forecast_container_wrapper = ft.Container(
            content=self.forecast_row,
            visible=False,
            animate_scale=self.pop_animation,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN),
            scale=0.9,
            opacity=0,
        )

    def _build_error_display(self):
        """Initialize error message controls."""
        self.error_text = ft.Text(
            "Error message goes here",
            color=ft.Colors.RED_900,
            font_family="Montserrat",
            size=13,
            weight=ft.FontWeight.W_500,
            expand=True
        )
        
        self.error_icon = ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_700, size=24)
        
        self.error_container = ft.Container(
            content=ft.Row(
                [
                    self.error_icon,
                    self.error_text,
                    ft.IconButton(
                        ft.Icons.CLOSE, 
                        icon_size=18, 
                        icon_color=ft.Colors.RED_700,
                        on_click=lambda e: self.hide_error()
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.RED_50,
            border=ft.border.all(1, ft.Colors.RED_200),
            border_radius=10,
            padding=ft.padding.only(left=10, right=5, top=5, bottom=5),
            margin=ft.margin.only(bottom=10),
            animate_opacity=self.error_animation,
            animate_scale=self.error_animation,
            visible=False,
            opacity=0,
            offset=ft.Offset(0, -0.5), 
            animate_offset=self.error_animation
        )

    def build_ui(self):
        """Orchestrate UI assembly using helper methods."""
        header_row = self._build_header()
        search_row = self._build_search_controls()
        self._build_current_weather_display()
        self._build_forecast_display()
        self._build_error_display()
        
        self.loading = ft.ProgressRing(visible=False)
        
        main_content = ft.Column(
            [
                ft.Column([ft.Container(content=header_row, alignment=ft.alignment.center_left), search_row], spacing=10),
                self.loading,
                self.error_container,
                ft.Column(
                    [
                        self.weather_container, 
                        self.humidity_wind_container,
                        self.forecast_container_wrapper 
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8, 
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            scroll=ft.ScrollMode.AUTO 
        )

        self.page.add(
            ft.SafeArea(
                ft.Container(
                    content=main_content, 
                    padding=20, 
                    expand=True
                ),
                expand=True
            )
        )

    # --- Logic Methods ---

    def load_history(self):
        if self.history_file.exists():
            try:
                with self.history_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list): 
                        return data
            except (json.JSONDecodeError, OSError) as e:
                print(f"Error loading history: {e}")
                return []
        return []

    def save_history(self):
        try:
            with self.history_file.open("w", encoding="utf-8") as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e: 
            print(f"History Save Error: {e}")

    def add_to_history(self, city: str):
        city = city.strip()
        if not city:
            return
        
        if city in self.search_history:
            self.search_history.remove(city)
            
        self.search_history.insert(0, city)
        self.search_history = self.search_history[:10]
        self.save_history()
        self.refresh_searchbar_controls()

    def build_searchbar_controls(self):
        if not self.search_history:
            return [
                ft.ListTile(
                    title=ft.Text("No recent searches", size=14, italic=True, color=ft.Colors.GREY_500),
                    leading=ft.Icon(ft.Icons.HISTORY_TOGGLE_OFF, color=ft.Colors.GREY_500),
                    disabled=True,
                    height=50  
                )
            ]
            
        return [
            ft.ListTile(
                title=ft.Text(city), 
                leading=ft.Icon(ft.Icons.HISTORY),
                data=city, 
                on_click=self.on_history_click,
                height=50  
            ) 
            for city in self.search_history
        ]

    def refresh_searchbar_controls(self):
        if not hasattr(self, "city_input"):
            return
        
        # Update controls
        self.city_input.controls = self.build_searchbar_controls()
        
        # Height calculation
        header_height = 70 
        item_height = 50
        item_count = len(self.search_history) if self.search_history else 1
        visible_items = min(item_count, 5)
        calculated_height = header_height + (visible_items * item_height) + 20

        # Apply height
        self.city_input.view_height = calculated_height
        
        if self.city_input.page:
            self.city_input.update()

    # Theme Logic
    def create_themed_text(self, value, size, weight=None, italic=False):
        """Helper to create text and register it for theme updates."""
        t = ft.Text(
            value, size=size, weight=weight, italic=italic, font_family="Montserrat",
            color=ft.Colors.BLACK if not self.is_dark_mode else ft.Colors.WHITE,
            animate_opacity=300,
        )
        self.text_elements.append(t)
        return t

    def get_weather_gradient(self, condition):
        if self.is_dark_mode:
            gradients = {
                "Clear": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#1A237E", "#311B92"]),
                "Clouds": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#455A64", "#263238"]),
                "Rain": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#37474F", "#102027"]),
                "Snow": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#78909C", "#455A64"]),
                "Thunderstorm": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#212121", "#000000"]),
                "Drizzle": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#37474F", "#263238"]),
                "Mist": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#546E7A", "#37474F"]),
                "Haze": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#546E7A", "#37474F"]),
            }
        else:
             gradients = {
                "Clear": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.LIGHT_BLUE_200, ft.Colors.BLUE_400]),
                "Clouds": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.BLUE_GREY_100, ft.Colors.BLUE_GREY_400]),
                "Rain": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.BLUE_GREY_400, ft.Colors.GREY_700]),
                "Snow": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.WHITE, ft.Colors.LIGHT_BLUE_100]),
                "Thunderstorm": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.DEEP_PURPLE_700, ft.Colors.GREY_900]),
                "Drizzle": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.LIGHT_BLUE_200, ft.Colors.BLUE_GREY_200]),
                "Mist": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.GREY_300, ft.Colors.GREY_500]),
                "Haze": ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ft.Colors.GREY_300, ft.Colors.GREY_500]),
            }
        return gradients.get(condition, gradients["Clear"])

    def toggle_theme(self, e):
        self.is_dark_mode = not self.is_dark_mode
        
        # Toggle Theme Mode
        if self.is_dark_mode:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_menu_item.icon = ft.Icons.LIGHT_MODE
            self.theme_menu_item.text = "Light Mode"
            
            self.page.bgcolor = "#121212" 
            card_bg = "#212529"
            text_color = ft.Colors.WHITE
            current_shadow = None 
            
            # Update Buttons
            self.search_button.bgcolor = "#212529" 
            self.search_icon.color = ft.Colors.WHITE 
            
            self.gps_button.bgcolor = "#212529"
            self.gps_icon.color = ft.Colors.WHITE
            
            self.city_input.view_bgcolor = "#212529"
            
            # Update Error Container for Dark Mode
            self.error_container.bgcolor = "#3E1A1A" # Dark Red
            self.error_container.border = ft.border.all(1, "#EF5350")
            self.error_text.color = "#FFCDD2" # Light Red Text
            self.error_icon.color = "#EF5350"
            
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_menu_item.icon = ft.Icons.DARK_MODE
            self.theme_menu_item.text = "Dark Mode"

            self.page.bgcolor = ft.Colors.WHITE
            card_bg = ft.Colors.WHITE
            text_color = ft.Colors.BLUE_900
            current_shadow = self.card_shadow 

            # Update Buttons
            self.search_button.bgcolor = ft.Colors.BLUE_50 
            self.search_icon.color = ft.Colors.BLUE_700 
            
            self.gps_button.bgcolor = ft.Colors.BLUE_50
            self.gps_icon.color = ft.Colors.BLUE_700
            
            self.city_input.view_bgcolor = ft.Colors.WHITE

            # Update Error Container for Light Mode
            self.error_container.bgcolor = ft.Colors.RED_50
            self.error_container.border = ft.border.all(1, ft.Colors.RED_200)
            self.error_text.color = ft.Colors.RED_900
            self.error_icon.color = ft.Colors.RED_700

        # Update Cards
        for card in self.card_containers:
            card.bgcolor = card_bg
            card.shadow = current_shadow
            
        # Update Text
        for text in self.text_elements:
            text.color = text_color

        # Update Container Gradient
        if self.current_weather_data:
            self.weather_container.gradient = self.get_weather_gradient(self.current_condition_main)
            self.weather_container.bgcolor = None
        else:
            self.weather_container.gradient = None
            self.weather_container.bgcolor = ft.Colors.BLUE_50 if not self.is_dark_mode else "#212529"

        self.page.update()

    # Geolocation Logic
    async def on_gps_click(self, e):
        """Triggered when GPS button is clicked."""
        self.loading.visible = True
        self.hide_error()
        
        # Hide existing data
        for control in [self.weather_container, self.humidity_wind_container, self.forecast_container_wrapper]:
            control.visible = False
            control.opacity = 0
        self.page.update()

        try:
            # Request Permission
            permission = await self.geolocator.request_permission_async()
            
            if permission == ft.GeolocatorPermissionStatus.DENIED:
                 self.show_error("Location permission denied.")
                 return

            # Get Position
            position = await self.geolocator.get_current_position_async(
                accuracy=ft.GeolocatorPositionAccuracy.LOW
            )

            if position:
                print(f"GPS: {position.latitude}, {position.longitude}")
                await self.fetch_weather_by_coords(position.latitude, position.longitude)
            else:
                print("GPS timed out, trying IP fallback...")
                await self.get_ip_location_weather()

        except Exception as e:
            print(f"GPS Error: {e}")
            await self.get_ip_location_weather()

    def on_gps_position(self, e):
        """Callback when Native GPS successfully gets coordinates."""
        print(f"GPS Coordinates: {e.latitude}, {e.longitude}")
        self.page.run_task(self.fetch_weather_by_coords, e.latitude, e.longitude)

    def on_gps_error(self, e):
        """Callback when Native GPS fails (permission denied/timeout)."""
        print(f"GPS Error: {e}. Falling back to IP.")
        self.page.run_task(self.get_ip_location_weather)

    async def get_ip_location_weather(self):
        """Fallback: Get weather based on IP address using Config URL."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(Config.IP_API_URL)
                if response.status_code == 200:
                    data = response.json()
                    lat = data.get('latitude')
                    lon = data.get('longitude')
                    if lat and lon:
                        await self.fetch_weather_by_coords(lat, lon)
                    else:
                        raise Exception("Invalid location data")
                else:
                    raise Exception("Could not determine location")
        except Exception as e:
            self.loading.visible = False
            self.show_error(f"Location failed: {str(e)}")

    async def fetch_weather_by_coords(self, lat, lon):
        """Orchestrator to fetch weather and forecast using coordinates."""
        try:
            # Fetch Data
            weather_task = self.weather_service.get_weather_by_coordinates(lat, lon)
            forecast_task = self.weather_service.get_forecast_by_coordinates(lat, lon)
            
            weather_data, forecast_data = await asyncio.gather(weather_task, forecast_task)
            
            self.current_weather_data = weather_data
            
            # Update UI
            await self.display_weather(weather_data, animate=False)
            await self.process_and_display_forecast(forecast_data, animate=False)

            # Update Search Bar
            detected_city = weather_data.get("name", "")
            if detected_city:
                self.city_input.value = detected_city
                self.add_to_history(detected_city)

            self.loading.visible = False
            self.page.update()
            
            # Trigger Animations
            await self.animate_show_control(self.weather_container)
            await asyncio.sleep(0.2)
            await self.animate_show_control(self.humidity_wind_container)
            await asyncio.sleep(0.2)
            await self.animate_show_control(self.forecast_container_wrapper)

        except Exception as e:
            self.loading.visible = False
            self.show_error(str(e))

    # Unit Conversion
    async def toggle_unit(self, e):
        # Fade Out
        self.main_temp_text.opacity = 0
        self.feels_like_text.opacity = 0
        self.high_low_text.opacity = 0
        
        for item in self.forecast_text_controls:
            item['control'].opacity = 0
            
        self.page.update()
        
        await asyncio.sleep(0.3)

        # Update Data
        self.is_celsius = not self.is_celsius
        
        if self.is_celsius:
            self.unit_menu_item.text = "Switch to °F"
        else:
            self.unit_menu_item.text = "Switch to °C"

        if self.current_weather_data:
            self.update_weather_values()
        if self.forecast_text_controls:
            self.update_forecast_values()
            
        # Fade In
        self.main_temp_text.opacity = 1
        self.feels_like_text.opacity = 1
        self.high_low_text.opacity = 1
        
        for item in self.forecast_text_controls:
            item['control'].opacity = 1
            
        self.page.update()

    def convert_temp_val(self, temp_c):
        if self.is_celsius:
            return temp_c
        return (temp_c * 9/5) + 32

    def calculate_temp(self, temp_c):
        val = self.convert_temp_val(temp_c)
        unit = "°C" if self.is_celsius else "°F"
        return f"{val:.1f}{unit}"

    def update_weather_values(self):
        if not self.current_weather_data:
            return
        data = self.current_weather_data
        main_data = data.get("main", {})
        
        temp_c = main_data.get("temp", 0)
        feels_like_c = main_data.get("feels_like", 0)

        self.main_temp_text.value = self.calculate_temp(temp_c)
        self.feels_like_text.value = f"Feels like {self.calculate_temp(feels_like_c)}"
        
        if self.daily_high_c is not None and self.daily_low_c is not None:
            val_high = self.calculate_temp(self.daily_high_c)
            val_low = self.calculate_temp(self.daily_low_c)
            self.high_low_text.value = f"↑ {val_high}   ↓ {val_low}"
        else:
            self.high_low_text.value = ""

    def update_forecast_values(self):
        for item in self.forecast_text_controls:
            high_c = item['high']
            low_c = item['low']
            control = item['control']
            val_h = int(round(self.convert_temp_val(high_c)))
            val_l = int(round(self.convert_temp_val(low_c)))
            control.value = f"{val_h}°/{val_l}°"

    # Search Logic
    def on_search(self, e):
        self.perform_search(self.city_input.value or "")

    def perform_search(self, city: str):
        city = city.strip()
        if not city:
            self.show_error("Please enter a city name")
            return
        self.city_input.value = city
        self.hide_error()
        self.page.update()
        self.page.run_task(self.get_weather)

    def on_city_tap(self, e):
        self.city_input.open_view()

    def on_city_submit(self, e):
        city = (e.data or "").strip()
        if not city:
            return
        self.city_input.close_view(city)
        self.perform_search(city)

    def on_history_click(self, e):
        city = e.control.data
        self.city_input.close_view(city)
        self.perform_search(city)

    # Data Fetching
    async def get_weather(self):
        city = self.city_input.value.strip()
        if not city:
            self.show_error("Please enter a city name")
            return

        self.add_to_history(city)
        self.loading.visible = True
        self.hide_error()
        
        # Reset UI
        for control in [self.weather_container, self.humidity_wind_container, self.forecast_container_wrapper]:
            control.visible = False
            control.scale = 0.9
            control.opacity = 0
            
        self.page.update()

        try:
            # Fetch Data
            weather_task = self.weather_service.get_weather(city)
            forecast_task = self.weather_service.get_forecast(city)
            weather_data, forecast_data = await asyncio.gather(weather_task, forecast_task)
            
            self.current_weather_data = weather_data
            
            # Update UI
            await self.display_weather(weather_data, animate=False)
            await self.process_and_display_forecast(forecast_data, animate=False)

            self.loading.visible = False
            self.page.update()
            
            # Animate Elements
            await self.animate_show_control(self.weather_container)
            await asyncio.sleep(0.2) 
            await self.animate_show_control(self.humidity_wind_container)
            await asyncio.sleep(0.2) 
            await self.animate_show_control(self.forecast_container_wrapper)

        except Exception as e:
            self.loading.visible = False
            self.show_error(str(e))
    
    # Display Logic
    async def display_weather(self, data: dict, animate=True):
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        self.current_condition_main = data.get("weather", [{}])[0].get("main", "Clear")
        
        humidity = data.get("main", {}).get("humidity", 0)
        pressure = data.get("main", {}).get("pressure", 0)
        cloudiness = data.get("clouds", {}).get("all", 0)
        wind_speed = data.get("wind", {}).get("speed", 0)

        self.location_text.value = f"{city_name}, {country}"
        self.desc_text.value = description
        self.humidity_value_text.value = f"{humidity}%"
        self.wind_value_text.value = f"{wind_speed} m/s"
        self.pressure_value_text.value = f"{pressure} hPa"
        self.cloud_value_text.value = f"{cloudiness}%"
        
        self.daily_high_c = None
        self.daily_low_c = None
        
        self.update_weather_values()

        self.weather_container.gradient = self.get_weather_gradient(self.current_condition_main)
        self.weather_container.bgcolor = None 

        self.weather_container.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.LOCATION_ON, size=24, color=ft.Colors.WHITE), 
                        self.location_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8,
                ),
                ft.Image(src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png", width=90, height=90),
                ft.Container(height=4),
                self.desc_text,
                ft.Container(height=8),
                self.main_temp_text,
                ft.Container(height=4),
                self.feels_like_text,
                ft.Container(height=8),
                self.high_low_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            spacing=0, 
        )
        
        if animate:
            self.weather_container.visible = True
            self.humidity_wind_container.visible = True

    async def process_and_display_forecast(self, data: dict, animate=True):
        raw_list = data.get("list", [])
        daily_groups = defaultdict(lambda: {"temps": [], "icons": [], "dt": 0})
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # Group by Date
        for item in raw_list:
            ts = item.get("dt")
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            
            temp = item.get("main", {}).get("temp")
            icon = item.get("weather", [{}])[0].get("icon")
            
            daily_groups[date_str]["temps"].append(temp)
            daily_groups[date_str]["icons"].append(icon)
            daily_groups[date_str]["dt"] = ts

        current_temp = self.current_weather_data.get("main", {}).get("temp", 0)

        # Calculate Daily High/Low
        if today_str in daily_groups:
            today_temps = daily_groups[today_str]["temps"]
            self.daily_high_c = max(today_temps + [current_temp])
            self.daily_low_c = min(today_temps + [current_temp])
        else:
            self.daily_high_c = current_temp
            self.daily_low_c = current_temp

        self.update_weather_values()

        # Build Cards
        sorted_dates = sorted(daily_groups.keys())
        forecast_days = sorted_dates[:5]
        
        self.forecast_row.controls.clear()
        self.forecast_text_controls.clear() 

        for date_str in forecast_days:
            day_data = daily_groups[date_str]
            
            if date_str == today_str and self.daily_high_c is not None:
                high_temp = self.daily_high_c
                low_temp = self.daily_low_c
            else:
                high_temp = max(day_data["temps"])
                low_temp = min(day_data["temps"])

            mid_index = len(day_data["icons"]) // 2
            icon_code = day_data["icons"][mid_index]
            
            ts = day_data["dt"]
            dt_obj = datetime.fromtimestamp(ts)
            day_name = dt_obj.strftime("%a")
            
            self.create_forecast_card(day_name, icon_code, high_temp, low_temp)
    
        self.update_forecast_values()
        
        if animate:
            self.forecast_container_wrapper.visible = True
            self.page.update()

    async def animate_show_control(self, control):
        """Resets and then animates a control into view."""
        # Set initial state
        control.visible = True
        control.scale = 0.9
        control.opacity = 0
        control.update()
        
        await asyncio.sleep(0.05)
        
        # Trigger animation
        control.scale = 1.0
        control.opacity = 1.0
        control.update()

    def create_forecast_card(self, day_name, icon_code, high_c, low_c):
        day_text = self.create_themed_text(day_name, size=14, weight=ft.FontWeight.W_600)
        temp_text = self.create_themed_text("", size=14, weight=ft.FontWeight.BOLD) 
        
        self.forecast_text_controls.append({
            "high": high_c,
            "low": low_c,
            "control": temp_text
        })

        card = ft.Container(
            width=64.14,
            height=154,
            bgcolor=ft.Colors.WHITE if not self.is_dark_mode else "#212529",
            border_radius=10, 
            shadow=self.card_shadow if not self.is_dark_mode else None,
            padding=ft.padding.symmetric(vertical=10),
            animate=self.theme_animation,
            content=ft.Column(
                [
                    day_text,
                    ft.Image(src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png", width=48, height=48),
                    temp_text
                ],
                spacing=19,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        self.card_containers.append(card)
        self.forecast_row.controls.append(card)

    def show_error(self, message: str):
        # Update text
        self.error_text.value = message
        
        # Hide other containers
        self.weather_container.visible = False
        self.humidity_wind_container.visible = False
        self.forecast_container_wrapper.visible = False
        
        # Show Error Container
        self.error_container.visible = True
        self.error_container.opacity = 1
        self.error_container.offset = ft.Offset(0, 0)
        self.error_container.scale = 1.0
        self.page.update()

    def hide_error(self):
        """Hide the error container smoothly."""
        self.error_container.opacity = 0
        self.error_container.offset = ft.Offset(0, -0.5)
        self.error_container.scale = 0.95
        self.error_container.visible = False
        self.page.update()
        
    def create_metric_card(self, icon, label, value_text: ft.Text, icon_color):
        label_text = self.create_themed_text(label, size=12, weight=ft.FontWeight.W_500, italic=True)
        label_text.text_align = ft.TextAlign.CENTER

        container = ft.Container(
            width=169, height=115, padding=8, 
            bgcolor=ft.Colors.WHITE if not self.is_dark_mode else "#212529", 
            border_radius=10,
            shadow=self.card_shadow if not self.is_dark_mode else None,
            animate=self.theme_animation,
            content=ft.Column(
                [
                    ft.Icon(icon, size=48, color=icon_color),
                    label_text,
                    value_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8,
            ),
        )
        self.card_containers.append(container)
        return container

def main(page: ft.Page):
    WeatherApp(page)

if __name__ == "__main__":
    ft.app(target=main)