# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def validate_contact_fields(field, field_name, field_val, page):
    """Validates the contact fields with custom validation logic."""
    field.error_text = None
    
    if field_name == "name":
        name_val = field_val.strip()
        if not name_val:
            field.error_text = "Name cannot be empty!"
        elif not all(char.isalpha() or char.isspace() or char in "-'" for char in name_val):
            field.error_text = "Name can only contain letters!"
    
    elif field_name == "phone":
        clean_phone = ''.join(char for char in field_val if char.isdigit())
        if clean_phone.startswith("0"):
            clean_phone = clean_phone[1:]
        
        if clean_phone != field_val:
            field.value = clean_phone
        
        if not clean_phone:
            field.error_text = "Phone number cannot be empty!"
        elif not clean_phone.startswith("9"):
            field.error_text = "Phone number must start with 9!"
        elif len(clean_phone) != 10:
            field.error_text = "Phone number must be 10 digits!"
    
    elif field_name == "email":
        email_val = field_val.strip()
        if not email_val:
            field.error_text = "Email cannot be empty!"
        else:
            at_parts = email_val.split("@")
            if not (len(at_parts) == 2 and at_parts[0] and at_parts[1] and 
                   "." in at_parts[1] and not email_val.endswith(".") and 
                   not at_parts[1].startswith(".")):
                field.error_text = "Please enter a valid email address!"
    
    page.update()

def display_contacts(page, contacts_list_view, db_conn, search_query=""):
    """Fetches and displays all contacts in a modern card layout."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_query)
    
    # Sort contacts alphabetically by name
    contacts = sorted(contacts, key=lambda x: x[1].lower())
    
    # Determine theme colors
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    card_bg = "#192536" if is_dark else "#E3F2FD"
    text_color = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    icon_color = "#1d7ed3" if is_dark else "#1976D2"

    for contact in contacts:
        contact_id, name, phone, email = contact
        
        contacts_list_view.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=ft.padding.all(6),
                    bgcolor=card_bg,
                    border_radius=8,
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON, size=43, color=icon_color),
                                padding=ft.padding.all(8),
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [
                                    ft.Text(name, weight=ft.FontWeight.BOLD, size=14, color=text_color),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PHONE, size=14, color=icon_color),
                                            ft.Text(phone, color=text_color),
                                        ],
                                        spacing=8
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.EMAIL, size=14, color=icon_color),
                                            ft.Text(email, color=text_color),
                                        ],
                                        spacing=8
                                    ),
                                ],
                                expand=True,
                                spacing=2,
                            ),
                            ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                icon_color=text_color,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Edit",
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view, search_query)
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        text="Delete",
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda _, cid=contact_id: confirm_delete_dialog(page, cid, name, db_conn, contacts_list_view, search_query)
                                    ),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
            )
        )
    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn, search_query=""):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs
    
    # Validate all fields
    for field, field_name in [(name_input, "name"), (phone_input, "phone"), (email_input, "email")]:
        validate_contact_fields(field, field_name, field.value, page)
    
    # Check if any field has errors
    if any(field.error_text for field in inputs):
        return
    
    # Format phone number with +63 prefix
    phone_digits = ''.join(char for char in phone_input.value if char.isdigit())
    formatted_phone = f"+63{phone_digits}"
    
    add_contact_db(db_conn, name_input.value.strip(), formatted_phone, email_input.value.strip())
    
    for field in inputs:
        field.value = ""
        
    display_contacts(page, contacts_list_view, db_conn, search_query)
    page.update()

def delete_contact(page, contact_id, db_conn, contacts_list_view, search_query=""):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view, db_conn, search_query)

def open_edit_dialog(page, contact, db_conn, contacts_list_view, search_query=""):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    # Create compact text fields with proper sizing
    edit_name = ft.TextField(
        label="Name",
        value=name,
        width=300,
        hint_text="Juan Doe",
        hint_style=ft.TextStyle(color=ft.Colors.GREY, size=14),
        autofill_hints=ft.AutofillHint.NAME,
    )

    # Extract digits from the stored phone number (remove +63 prefix)
    phone_digits = ''.join(char for char in phone if char.isdigit())
    # Remove the leading 63 if present (since we store +63XXXXXXXXXX)
    if phone_digits.startswith("63"):
        phone_digits = phone_digits[2:]
    
    edit_phone = ft.TextField(
        label="Phone",
        value=phone_digits,
        width=300,
        prefix_text="+63 ",
        prefix_style=ft.TextStyle(size=14),
        hint_text="9XXXXXXXXX",
        hint_style=ft.TextStyle(color=ft.Colors.GREY, size=14),
        autofill_hints=ft.AutofillHint.TELEPHONE_NUMBER,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d{0,10}$"),
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    edit_email = ft.TextField(
        label="Email",
        value=email,
        width=300,
        hint_text="abc123@domain.com",
        hint_style=ft.TextStyle(color=ft.Colors.GREY, size=14),
        autofill_hints=ft.AutofillHint.EMAIL,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[a-zA-Z0-9@._-]*$"),
    )

    # Add validation handlers
    for field, key in [(edit_name, "name"), (edit_phone, "phone"), (edit_email, "email")]:
        field.on_change = lambda e, f=field, k=key: validate_contact_fields(f, k, f.value, page)
        field.on_blur = lambda e, f=field, k=key: validate_contact_fields(f, k, f.value, page)

    # Success dialog
    success_dialog = ft.AlertDialog(
        icon=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.GREEN),
        title=ft.Text("Contact Updated", text_align=ft.TextAlign.CENTER),
        content=ft.Text(
            spans=[
                ft.TextSpan("Contact "),
                ft.TextSpan(name.upper(), style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=16)),
                ft.TextSpan(" successfully updated!")
            ],
            text_align=ft.TextAlign.CENTER
        ),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close(success_dialog) or page.update())]
    )

    # Field error dialog
    field_error_dialog = ft.AlertDialog(
        icon=ft.Icon(ft.Icons.ERROR_ROUNDED, color=ft.Colors.RED),
        title=ft.Text("Error Updating Contact", text_align=ft.TextAlign.CENTER),
        content=ft.Text("Please check input fields for errors.", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: page.open(edit_dialog) or page.update())]
    )

    # Input required dialog
    input_required_dialog = ft.AlertDialog(
        icon=ft.Icon(ft.Icons.ERROR_ROUNDED, color=ft.Colors.RED),
        title=ft.Text("Error Updating Contact", text_align=ft.TextAlign.CENTER),
        content=ft.Text("All fields are required.", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: page.open(edit_dialog) or page.update())]
    )

    # System error dialog
    system_error_dialog = ft.AlertDialog(
        icon=ft.Icon(ft.Icons.ERROR_ROUNDED, color=ft.Colors.RED),
        title=ft.Text("Error Updating Contact"),
        content=ft.Text("An unexpected error occurred. Please try again later.", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close(system_error_dialog) or page.update())]
    )

    def save_and_close(e):
        # Check for validation errors
        if edit_name.error_text or edit_phone.error_text or edit_email.error_text:
            page.open(field_error_dialog)
            page.update()
            return

        # Check if all fields are filled
        if not (edit_name.value and edit_phone.value and edit_email.value):
            page.open(input_required_dialog)
            page.update()
            return

        try:
            # Format phone number with +63 prefix before saving
            phone_digits = ''.join(char for char in edit_phone.value if char.isdigit())
            formatted_phone = f"+63{phone_digits}"
            update_contact_db(db_conn, contact_id, edit_name.value, formatted_phone, edit_email.value)
            
            page.close(edit_dialog)
            page.update()
            
            page.open(success_dialog)
            page.update()
            
            display_contacts(page, contacts_list_view, db_conn, search_query)
            
        except Exception:
            page.close(edit_dialog)
            page.open(system_error_dialog)
            page.update()
            return

    # Create compact edit dialog
    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Update Contact Details", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [edit_name, edit_phone, edit_email],
            spacing=10,
            tight=True
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    edit_dialog.open = True
    page.overlay.append(edit_dialog)
    page.update()

def confirm_delete_dialog(page, contact_id, name, db_conn, contacts_list_view, search_query=""):
    """Opens a confirmation dialog before deleting a contact."""
    
    def confirm_delete(e):
        delete_contact(page, contact_id, db_conn, contacts_list_view, search_query)
        
        # Success dialog
        deleted_successfully_dialog = ft.AlertDialog(
            modal=True,
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.GREEN),
            title=ft.Text("Contact Deleted", text_align=ft.TextAlign.CENTER),
            content=ft.Text(
                spans=[
                    ft.TextSpan("Contact "),
                    ft.TextSpan(name.upper(), style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=16)),
                    ft.TextSpan(" successfully deleted!")
                ],
                text_align=ft.TextAlign.CENTER
            ),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close(deleted_successfully_dialog) or page.update())]
        )
        
        page.open(deleted_successfully_dialog)
        page.update()

    # Confirmation dialog
    confirm_dialog = ft.AlertDialog(
        modal=True,
        icon=ft.Icon(ft.Icons.WARNING_ROUNDED, color=ft.Colors.ORANGE),
        title=ft.Text("Confirm Deletion", text_align=ft.TextAlign.CENTER),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("No", on_click=lambda e: page.close(confirm_dialog) or page.update()),
            ft.TextButton("Yes", on_click=confirm_delete)
        ]
    )

    page.open(confirm_dialog)
    page.update()

def toggle_theme(page, ui_elements, e):
    """Toggle between light and dark theme modes."""
    if page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    # Update colors based on theme mode
    update_theme_colors(page, ui_elements)
    page.update()

def update_theme_colors(page, ui_elements):
    """Update all UI element colors based on current theme mode"""
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    
    # Unpack UI elements
    (appbar, appbar_title, appbar_icon, theme_button, 
     name_input, phone_input, email_input, search_input,
     add_contact_container, add_contact_title,
     all_contacts_container, all_contacts_text, all_contacts_icon,
     search_button_container, search_text, search_icon,
     contacts_list_view, db_conn) = ui_elements
    
    # Update appbar colors
    appbar.bgcolor = "#192536" if is_dark else "#1D7ED3"
    appbar_title.color = ft.Colors.WHITE if is_dark else ft.Colors.WHITE
    appbar_icon.color = ft.Colors.WHITE if is_dark else ft.Colors.WHITE
    theme_button.icon_color = ft.Colors.WHITE if is_dark else ft.Colors.WHITE
    theme_button.icon = ft.Icons.DARK_MODE if is_dark else ft.Icons.LIGHT_MODE
    
    # Update text input colors
    input_bg = "white" if is_dark else "white"
    input_text_color = "black" if is_dark else "black"
    
    for input_field in [name_input, phone_input, email_input]:
        input_field.bgcolor = input_bg
        input_field.color = input_text_color
    
    # Update search input
    search_input.bgcolor = input_bg
    search_input.color = input_text_color
    
    # Update add contact section
    add_contact_container.bgcolor = "#1D7ED3" if is_dark else "#E3F2FD"
    add_contact_title.color = ft.Colors.WHITE if is_dark else "#1976D2"
    
    # Update all contacts header
    all_contacts_container.bgcolor = "#192536" if is_dark else "#E3F2FD"
    all_contacts_text.color = ft.Colors.WHITE if is_dark else "#1976D2"
    all_contacts_icon.color = ft.Colors.WHITE if is_dark else "#1976D2"
    
    # Update search button
    search_button_container.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE) if is_dark else ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
    search_text.color = ft.Colors.BLUE_GREY_300 if is_dark else ft.Colors.BLUE_GREY_600
    search_icon.color = ft.Colors.BLUE_GREY_300 if is_dark else ft.Colors.BLUE_GREY_600
    
    # Refresh contacts display
    display_contacts(page, contacts_list_view, db_conn)

def check_item_clicked(page, e):
    """Handle checkbox click events."""
    e.control.checked = not e.control.checked
    page.update()

def toggle_search(page, search_visible, search_container, search_input, contacts_list_view, db_conn, e):
    """Toggle search visibility and reset search when closed."""
    search_visible = not search_visible
    if search_visible:
        search_container.visible = True
        search_input.value = ""
    else:
        search_container.visible = False
        search_input.value = ""
        # Reset to show all contacts when search is closed
        display_contacts(page, contacts_list_view, db_conn)
    page.update()
    return search_visible