import reflex as rx

config = rx.Config(
    app_name="portal",
    upload_dir="uploads",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)