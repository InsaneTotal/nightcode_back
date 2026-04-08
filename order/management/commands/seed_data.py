import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import OperationalError, ProgrammingError

from authinventory.models import Category
from authusers.models import Roles, Status, TypeDocument, User
from order.models import PaymentMethod, typeOrderStatus, typeStatusTables


class Command(BaseCommand):
    help = 'Carga datos base idempotentes para el proyecto.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-admin',
            action='store_true',
            help='Crea o actualiza un usuario administrador.',
        )
        parser.add_argument(
            '--admin-email', default=os.getenv('SEED_ADMIN_EMAIL', 'admin@nightcode.com'))
        parser.add_argument('--admin-password',
                            default=os.getenv('SEED_ADMIN_PASSWORD'))
        parser.add_argument('--admin-username',
                            default=os.getenv('SEED_ADMIN_USERNAME', 'admin'))
        parser.add_argument(
            '--admin-document', default=os.getenv('SEED_ADMIN_DOCUMENT', '1000000000'))
        parser.add_argument('--admin-first-name',
                            default=os.getenv('SEED_ADMIN_FIRST_NAME', 'Admin'))
        parser.add_argument(
            '--admin-last-name', default=os.getenv('SEED_ADMIN_LAST_NAME', 'NightCode'))

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            self._seed_type_documents()
            self._seed_roles()
            self._seed_user_statuses()
            self._seed_table_statuses()
            self._seed_order_statuses()
            self._seed_payment_methods()
            self._seed_categories()

            if options['with_admin']:
                self._seed_admin(options)
        except (OperationalError, ProgrammingError) as exc:
            raise CommandError(
                'No se pudieron cargar seeds porque faltan tablas. '
                'Ejecuta primero: python manage.py migrate'
            ) from exc

        self.stdout.write(self.style.SUCCESS('Seed completado correctamente.'))

    def _seed_type_documents(self):
        for name in ['CC', 'CE', 'NIT', 'PASAPORTE']:
            _, created = TypeDocument.objects.get_or_create(name=name)
            self._log_result(f'TypeDocument: {name}', created)

    def _seed_roles(self):
        for name in ['Administrador', 'Mesero', 'Bartender', 'Cliente']:
            _, created = Roles.objects.get_or_create(name=name)
            self._log_result(f'Role: {name}', created)

    def _seed_user_statuses(self):
        for name in ['Activo', 'Inactivo']:
            _, created = Status.objects.get_or_create(name=name)
            self._log_result(f'UserStatus: {name}', created)

    def _seed_table_statuses(self):
        for name in ['Disponible', 'Ocupada', 'Pendiente', 'Llamando mesero']:
            _, created = typeStatusTables.objects.get_or_create(name=name)
            self._log_result(f'TableStatus: {name}', created)

    def _seed_order_statuses(self):
        for name in ['Pendiente', 'En preparacion', 'Entregada', 'Pagada', 'Cancelada']:
            _, created = typeOrderStatus.objects.get_or_create(name=name)
            self._log_result(f'OrderStatus: {name}', created)

    def _seed_payment_methods(self):
        for name in ['Efectivo', 'Tarjeta', 'Transferencia']:
            _, created = PaymentMethod.objects.get_or_create(name=name)
            self._log_result(f'PaymentMethod: {name}', created)

    def _seed_categories(self):
        for name in ['Cervezas', 'Cocteles', 'Rones', 'Tequilas', 'Vinos', 'Vodkas', 'Whiskeys']:
            _, created = Category.objects.get_or_create(name=name)
            self._log_result(f'Category: {name}', created)

    def _seed_admin(self, options):
        admin_password = options['admin_password']
        if not admin_password:
            raise CommandError(
                'Falta --admin-password o variable SEED_ADMIN_PASSWORD para crear admin.'
            )

        role_admin = Roles.objects.get(name='Administrador')
        status_active = Status.objects.get(name='Activo')
        doc_type = TypeDocument.objects.get(name='CC')

        admin_email = options['admin_email'].strip().lower()

        user, created = User.objects.update_or_create(
            email=admin_email,
            defaults={
                'username': options['admin_username'].strip(),
                'first_name': options['admin_first_name'].strip(),
                'last_name': options['admin_last_name'].strip(),
                'document_number': options['admin_document'].strip(),
                'id_type_document': doc_type,
                'id_role': role_admin,
                'id_status': status_active,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        user.set_password(admin_password)
        user.save(update_fields=['password'])

        self._log_result(f'AdminUser: {admin_email}', created)

    def _log_result(self, label, created):
        action = 'CREATED' if created else 'EXISTS'
        self.stdout.write(f'[{action}] {label}')
