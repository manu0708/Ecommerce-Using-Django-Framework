JAZZMIN_SETTINGS = {
    "site_title": "MegaZon Admin",
    "site_header": "Admin Panel",
    "site_brand": "MegaZon Admin Page",
    "site_logo": "images/logo (2).png/",
    "welcome_sign": "Welcome to the MegaZon (E-commerce Application)",
    "copyright": "MegaZon",
    "user_avatar": "User.Profile.user_avatar",
     "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "VISIT TO MegaZon SITE", "url": "home", "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
    ],
    
}
