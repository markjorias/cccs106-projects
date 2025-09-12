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
    
    # Page Layout Configuration
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Page Background Color
    page.bgcolor = ft.Colors.AMBER_ACCENT
    
    # counter = ft.Text("0", size=50, data=0)

    # def increment_click(e):
    #     counter.data += 1
    #     counter.value = str(counter.data)
    #     counter.update()

    # page.floating_action_button = ft.FloatingActionButton(
    #     icon=ft.Icons.ADD, on_click=increment_click
    # )
    
    page.add(
        ft.Container(
            content = ft.Column(
                [
                    ft.Text(
                        "User Login",
                        font_family = "Google Sans Flex",
                        size = 24,
                        weight = ft.FontWeight.BOLD,
                        color = ft.Colors.BLACK
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
        )
    )
    )
    
    # page.add(
    #     ft.SafeArea(
    #         ft.Container(
    #             counter,
    #             alignment=ft.alignment.center,
    #         ),
    #         expand=True,
    #     )
    # )


ft.app(main)
