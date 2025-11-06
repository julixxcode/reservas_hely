from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Pago, Reserva

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/pagar/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def pagar(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)

    if request.method == 'POST':
        metodo = request.form.get('metodo')

        nuevo_pago = Pago(
            reserva_id=reserva.id,
            monto=reserva.habitacion.precio,
            metodo=metodo,
            estado='Aprobado (Simulado)'
        )
        reserva.estado = 'Pagada'
        db.session.add(nuevo_pago)
        db.session.commit()

        flash('Pago simulado realizado correctamente ✅', 'success')
        return redirect(url_for('booking.mis_reservas'))

    return render_template('payment.html', reserva=reserva)
