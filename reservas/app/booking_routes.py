from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Habitacion, Reserva

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/')
def index():
    """Página de inicio: redirige según el estado del usuario."""
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))

@booking_bp.route('/home')
@login_required
def home():
    """Página principal tras iniciar sesión."""
    return render_template('index.html')

@booking_bp.route('/search', methods=['GET', 'POST'])
@login_required
def buscar_habitaciones():
    """Permite buscar habitaciones disponibles por tipo y fecha."""
    habitaciones = []
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), "%Y-%m-%d")
        fecha_fin = datetime.strptime(request.form.get('fecha_fin'), "%Y-%m-%d")

        # Buscar habitaciones del tipo seleccionado y filtrar disponibilidad
        habitaciones_tipo = Habitacion.query.filter_by(tipo=tipo, disponible=True).all()
        disponibles = []

        for h in habitaciones_tipo:
            conflicto = Reserva.query.filter(
                Reserva.habitacion_id == h.id,
                Reserva.fecha_fin >= fecha_inicio,
                Reserva.fecha_inicio <= fecha_fin
            ).first()
            if not conflicto:
                disponibles.append(h)
        habitaciones = disponibles

    return render_template('search.html', habitaciones=habitaciones)

@booking_bp.route('/reservar/<int:habitacion_id>', methods=['GET', 'POST'])
@login_required
def reservar(habitacion_id):
    """Permite reservar una habitación seleccionada."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)

    if request.method == 'POST':
        fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), "%Y-%m-%d")
        fecha_fin = datetime.strptime(request.form.get('fecha_fin'), "%Y-%m-%d")

        nueva_reserva = Reserva(
            usuario_id=current_user.id,
            habitacion_id=habitacion.id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='Pendiente'
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        flash('Reserva creada correctamente. Procede al pago simulado.', 'success')
        return redirect(url_for('payment.pagar', reserva_id=nueva_reserva.id))

    return render_template('booking_confirm.html', habitacion=habitacion)

@booking_bp.route('/mis_reservas')
@login_required
def mis_reservas():
    """Muestra todas las reservas del usuario autenticado."""
    reservas = Reserva.query.filter_by(usuario_id=current_user.id).all()
    return render_template('profile.html', reservas=reservas)
