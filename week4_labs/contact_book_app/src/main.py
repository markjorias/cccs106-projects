# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, toggle_theme, update_theme_colors, toggle_search, validate_contact_fields

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width = 412
    page.window.height = 917
    page.window.frameless = True
    page.window.center()
    
    db_conn = init_db()
    
    # Create appbar elements
    appbar_title = ft.Text(" Contact Book", color="white", size=22, weight=ft.FontWeight.BOLD)
    appbar_icon = ft.Icon(ft.Icons.BOOK, color="white", size=36)
    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE,
        icon_size=24,
        on_click=lambda e: toggle_theme(page, ui_elements, e),
        tooltip="Toggle Dark/Light Mode",
        icon_color="white",
    )
    
    appbar = ft.Container(
        content=ft.Row(
            [
                ft.Row([appbar_icon, appbar_title], alignment=ft.MainAxisAlignment.START),
                ft.Container(content=theme_button, margin=ft.Margin(0, 0, 16, 0)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#192536",
        width=380,
        height=56,
        padding=ft.Padding(16, 0, 0, 0),
        alignment=ft.alignment.center,
        border_radius=8,
    )

    # Input fields
    name_input = ft.TextField(
        label="Name",
        hint_text="Juan Dela Cruz",
        icon=ft.Icons.PERSON_ROUNDED,
        width=349,
        content_padding=ft.padding.symmetric(vertical=16, horizontal=12),
        border_radius=16,
        bgcolor="white",
        color="black",
        on_change=lambda e: validate_contact_fields(name_input, "name", name_input.value, page),
    )
    
    phone_input = ft.TextField(
        label="Phone", 
        hint_text="9XX XXX XXXX",
        prefix_text="+63 ",
        icon=ft.Icons.PHONE_ANDROID_ROUNDED,
        width=349, 
        content_padding=ft.padding.symmetric(vertical=16, horizontal=12),
        max_length=10,
        input_filter=ft.NumbersOnlyInputFilter(),
        border_radius=16,
        bgcolor="white",
        color="black",
        on_change=lambda e: validate_contact_fields(phone_input, "phone", phone_input.value, page),
    )
    
    email_input = ft.TextField(
        label="Email",
        hint_text="juandelacruz@my.cspc.edu.ph",
        icon=ft.Icons.EMAIL_ROUNDED,
        width=349, 
        content_padding=ft.padding.symmetric(vertical=16, horizontal=12),
        border_radius=16,
        bgcolor="white",
        color="black",
        on_change=lambda e: validate_contact_fields(email_input, "email", email_input.value, page),
    )
    
    inputs = (name_input, phone_input, email_input)
    
    contacts_list_view = ft.ListView(
        expand=True, 
        spacing=2, 
        auto_scroll=False,
        width=380,
        height=400,
    )

    add_button = ft.ElevatedButton(
        text="Add",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_input.value if search_visible else ""),
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16, color="#008BEE", weight=ft.FontWeight.BOLD),
            padding=ft.Padding(29, 20, 29, 20),
            bgcolor="#F0F0F0",
            shape=ft.RoundedRectangleBorder(radius=16),
        ),
    )
    
    # Search functionality
    search_visible = False
    
    def search_toggle_handler(e):
        nonlocal search_visible
        search_visible = toggle_search(page, search_visible, search_container, search_input, contacts_list_view, db_conn, e)
    
    search_input = ft.TextField(
        label="Search Contacts", 
        width=350,
        bgcolor="white",
        color="black",
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, search_query=e.control.value)
    )
    
    search_container = ft.Container(
        content=search_input,
        alignment=ft.alignment.center,
        visible=False,
        margin=ft.margin.only(top=8, bottom=8),
    )
    
    # Add contact section
    add_contact_title = ft.Text("Add Contact:", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    add_contact_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=add_contact_title, alignment=ft.alignment.center),
                name_input,
                phone_input,
                email_input,
                ft.Row([add_button], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=16
        ),
        alignment=ft.alignment.center,
        bgcolor="#1D7ED3",
        width=380,
        height=348,
        padding=ft.Padding(16, 16, 16, 16),
        border_radius=16,
    )
    
    # All contacts header
    all_contacts_icon = ft.Icon(ft.Icons.PEOPLE, size=18, color=ft.Colors.WHITE)
    all_contacts_text = ft.Text("All Contacts", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    all_contacts_container = ft.Container(
        height=32,
        bgcolor="#192536",
        border_radius=8,
        #margin=ft.margin.only(top=8, bottom=8),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[all_contacts_icon, all_contacts_text],
        ),
        padding=ft.padding.only(top=6, bottom=6, left=8, right=12),
    )
    
    # Search button
    search_icon = ft.Icon(ft.Icons.SEARCH, size=18, color=ft.Colors.BLUE_GREY_300)
    search_text = ft.Text("Search", size=14, color=ft.Colors.BLUE_GREY_300, weight=ft.FontWeight.W_500)
    search_button_container = ft.Container(
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[search_icon, search_text]
        ),
        padding=ft.padding.only(left=8, right=8, top=4, bottom=4),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        height=30,
        on_click=search_toggle_handler,
    )

    # UI elements for theme functions
    ui_elements = (appbar, appbar_title, appbar_icon, theme_button, 
                   name_input, phone_input, email_input, search_input,
                   add_contact_container, add_contact_title,
                   all_contacts_container, all_contacts_text, all_contacts_icon,
                   search_button_container, search_text, search_icon,
                   contacts_list_view, db_conn)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(content=appbar, alignment=ft.alignment.center),
                    add_contact_container,
                    ft.Divider(thickness=0, opacity=0, height=0),
                    ft.Container(
                        width=380,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[all_contacts_container, search_button_container]
                        )
                    ),
                    search_container,
                    ft.Container(
                        content=contacts_list_view, 
                        alignment=ft.alignment.center,
                        #height=400,  # Set a fixed height for the scrollable area
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                    )
                ], 
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            margin=ft.Margin(8, 36, 8, 8),
        ),
    )
        
    display_contacts(page, contacts_list_view, db_conn)
    
if __name__ == "__main__":
    ft.app(target=main)