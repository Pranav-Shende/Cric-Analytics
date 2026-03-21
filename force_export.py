# import os
# import django
# from django.core import serializers
# from django.apps import apps

# # 1. Setup Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cricket_site.settings')
# django.setup()

# output_file = "cricket_data_full.json"
# app_name = 'stats' # Change this if your app folder is named differently

# print(f"🚀 Exporting ALL models from '{app_name}'...")

# try:
#     # 2. Automatically find every model in your app
#     app_config = apps.get_app_config(app_name)
#     all_models = app_config.get_models()
    
#     # 3. Pull every single row from every table
#     all_objects = []
#     for model in all_models:
#         all_objects.extend(list(model.objects.all()))
    
#     # 4. Serialize and Save
#     data = serializers.serialize("json", all_objects, indent=2)
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(data)
        
#     print(f"✅ Success! Full data saved to {output_file}")
#     print(f"📦 Total items exported: {len(all_objects)}")

# except Exception as e:
#     print(f"❌ Error: {e}")