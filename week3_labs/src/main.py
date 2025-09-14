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
    page.padding = ft.Padding(50, 35, 50, 20)
    
    # Page Layout Configuration
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Page Background Color
    page.bgcolor = ft.Colors.AMBER_ACCENT
    
    # Prevents darkmode color modification
    page.theme_mode = ft.ThemeMode.LIGHT
    
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
    
    # Common text field style
    # Preserves consistency and reduces redundancy
    field_style = {
        "label_style": ft.TextStyle(color=ft.Colors.BLACK87),
        "hint_style": ft.TextStyle(color=ft.Colors.BLACK87),
        "helper_style": ft.TextStyle(color=ft.Colors.with_opacity(0.7, ft.Colors.BLACK87)),
        "width": 300,
        "bgcolor": ft.Colors.LIGHT_BLUE_ACCENT,
        "focused_border_color": ft.Colors.BLUE_700,
    }
    
    # Username Input Field
    username_field = ft.TextField(
        label="User name",
        icon = ft.Icons.PERSON,
        hint_text="Enter your username",
        helper_text="This is your unique identifier",
        autofocus=True,
        disabled=False,
        **field_style
        
    )
    
    # Password Input Field
    password_field = ft.TextField(
        label="Password",
        icon = ft.Icons.PASSWORD,
        hint_text="Enter your password",
        helper_text="This is your secret key",
        autofocus=True,
        disabled=False,
        password=True,
        can_reveal_password=True,
        **field_style
    )

    # login button click function
    def login_click(e):
        # dialog popups for different scenarios
        success_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
            title=ft.Text("Login Successful!", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Welcome, " + username_field.value + "!", text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("OK", on_click=lambda e: page.close(success_dialog))
            ],
        )
        
        failure_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
            title=ft.Text("Login Failed", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("OK", on_click=lambda e: page.close(failure_dialog))
            ],
        )
        
        invalid_input_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.INFO_ROUNDED, color=ft.Colors.BLUE),
            title=ft.Text("Input Error", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_dialog))
            ],
        )
        
        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Text("An error occurred while connecting to the database"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: page.close(database_error_dialog))
            ],
        )
    
        # check if fields are empty
        if username_field.value == "" or password_field.value == "":
            page.open(invalid_input_dialog)
            return
        
        try:
            # connect to database
            conn = connect_db()
            if conn is None:
                page.open(database_error_dialog)
                page.update()
                return
            
            cursor = conn.cursor()

            # check if user exists in database
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username_field.value, password_field.value))

            result = cursor.fetchone() is not None

            cursor.close()
            conn.close()

            # show appropriate dialog based on result
            if result:
                page.open(success_dialog)

            else:
                page.open(failure_dialog)

            page.update()

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            page.open(database_error_dialog)
            page.update()

    # Login Button  
    login_button = ft.ElevatedButton(
        "Login",
        on_click = login_click,
        width = 100,
        icon = ft.Icons.LOGIN,
        style=ft.ButtonStyle(
            color='#5579a0',
            bgcolor=ft.Colors.WHITE, 
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK87,
                weight=ft.FontWeight.BOLD,)
        )
    )
    
    # add all components to page layout
    page.add(
        ft.Column(
            [
                ft.Container(
                    login_title,
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    content = ft.Column([username_field, password_field], spacing=20,)
                ),
                
                ft.Container(
                    content = login_button,
                    alignment=ft.alignment.bottom_right,
                    margin=ft.Margin(0,20,0,10),
                )
            ]
        )
    )

ft.app(main)