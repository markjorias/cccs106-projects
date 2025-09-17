# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    
    db_conn = init_db()
    
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()
    
    page.appbar = ft.AppBar(
        # leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        toolbar_height=75,
        title=ft.Text("Contact Book"),
        center_title=True,
        bgcolor=ft.Colors.AMBER_ACCENT,
        title_text_style=ft.TextStyle(
            size=24, 
            weight=ft.FontWeight.BOLD
            ),
        # actions=[
        #     ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
        #     ft.IconButton(ft.Icons.FILTER_3),
        #     ft.PopupMenuButton(
        #         items=[
        #             ft.PopupMenuItem(text="Item 1"),
        #             ft.PopupMenuItem(),  # divider
        #             ft.PopupMenuItem(
        #                 text="Checked item", checked=False, on_click=check_item_clicked
        #             ),
        #         ]
        #     ),
        # ],
    )

    name_input = ft.TextField(
        label="Name", 
        width=350)
    
    phone_input = ft.TextField(
        label="Phone", 
        width=350)
    
    email_input = ft.TextField(
        label="Email", 
        width=350)
    
    inputs = (name_input, phone_input, email_input)
    
    contacts_list_view = ft.ListView(
        expand=1, 
        spacing=10, 
        auto_scroll=True
        )
    
    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
    )
    
    search_input = ft.TextField(
        label="Search Contacts", 
        width=350,
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, search_query=e.control.value)
    )
    
    
    page.add(
        ft.Column(
            [
                ft.Container(
                    content = ft.Text(
                        "Enter Contact Details:",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    )
                    ,alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    content = ft.Column([name_input, phone_input, email_input,]),
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    content = add_button,
                    alignment=ft.alignment.center,
                ),
                
                ft.Divider(),
                
                ft.Container(
                    content = ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center,
                ), 
                
                                ft.Container(
                    content=search_input,
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    content= contacts_list_view,
                    alignment=ft.alignment.center,
                )
                ], 
        )
    )
        
    display_contacts(page, contacts_list_view, db_conn)
    
if __name__ == "__main__":
    ft.app(target=main)