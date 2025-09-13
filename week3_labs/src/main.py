import flet as ft
import mysql.connector
from db_connection import connect_db


def main(page: ft.Page):
    
    # Window Configuration
    page.title = "User Login"
    page.window.center()
    page.window.frameless = True
    page.window.height = 350
    page.window.width = 400
    page.padding = 30 # PADDING AROUND THE CONTENT SO BUTTON DOESN'T TOUCH THE EDGES
    
    # Page Layout Configuration
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Page Background Color
    page.bgcolor = ft.Colors.AMBER_ACCENT
    
    # User Interface Controls
    
    # Login Title
    login_title = ft.Text(
        "User Login",
        text_align=ft.TextAlign.CENTER,
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        color=ft.Colors.BLACK,
    )
    
    # Username Input Field
    username_field = ft.TextField(
        label="User name",
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        hint_text="Enter your username",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        helper_text="This is your unique identifier",
        helper_style=ft.TextStyle(color=ft.Colors.BLACK54),
        width=300,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        color=ft.Colors.BLACK87,
        border_color=ft.Colors.BLACK54,
    )
    
    # Password Input Field
    password_field = ft.TextField(
        label="Password",
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        hint_text="Enter your password",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        helper_text="This is your secret key",
        helper_style=ft.TextStyle(color=ft.Colors.BLACK54),
        width=300,
        password=True,
        can_reveal_password=True,
        color=ft.Colors.BLACK87,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        border_color=ft.Colors.BLACK54,
    )
    
    login_button = ft.ElevatedButton(
        "Login",
        on_click = lambda e: print("Login Clicked"),
        width = 100,
        icon = ft.Icons.LOGIN,
        style=ft.ButtonStyle(
            color=ft.Colors.BLUE_GREY, 
            bgcolor=ft.Colors.WHITE, 
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK87,
                weight=ft.FontWeight.BOLD,)
        )
    )
    
    page.add(
        ft.Container(
            content=ft.Column(
            [
                login_title,
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.PERSON, color = "#43474e"),
                        username_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.PASSWORD, color = "#43474e"),
                        password_field
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    )
    
    page.add(
        ft.Container(
            content = login_button,
            alignment=ft.alignment.bottom_right,
        )
    )

ft.app(main)