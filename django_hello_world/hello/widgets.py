from django.forms import DateField, CharField, FileField, TextInput, Textarea, Form, EmailField


class ContactForm(Form):
    first_name = CharField(max_length=255, label="Name")
    last_name = CharField(max_length=255, label="Last name")
    email = EmailField(label="Email")
    bio = CharField(widget=Textarea, label="Bio")
    contacts = CharField(max_length=255, label="Contacts")
    skype = CharField(max_length=255, label="Contacts")
    jabber = CharField(max_length=255, label="Jabber")
    other = CharField(widget=Textarea, label="Other")
    uploaded_file = FileField()
