from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        duration = int(request.form['duration'])
        rate = float(request.form['rate'])

        if amount <= 0 or duration <= 0 or rate <= 0:
            return render_template('index.html', error='Проверьте правильность введённых данных!')

        # формула расчета ежемесячных платежей
        monthly_rate = rate / 100 / 12
        monthly_payment = (amount * monthly_rate * (1 + monthly_rate) ** duration) / (
                (1 + monthly_rate) ** duration - 1)
        total_payment = monthly_payment * duration

        payments = []
        balance = amount

        # проходим по месяцам и заполняем список всех платежей
        for i in range(duration):
            interest = balance * monthly_rate
            principle = monthly_payment - interest
            balance -= principle

            payments.append({
                'month': i + 1,
                'payment': round(monthly_payment, 2),
                'interest': round(interest, 2),
                'principle': round(principle, 2),
                'balance': round(balance, 2)
            })

        # передаем результаты расчетов в шаблон
        return redirect(url_for('results', amount=amount, duration=duration, rate=rate, monthly_payment=monthly_payment,
                                total_payment=total_payment, payments=json.dumps(payments)))
    return render_template('index.html')


@app.route('/results')
def results():
    amount = request.args.get('amount')
    duration = request.args.get('duration')
    rate = request.args.get('rate')
    monthly_payment = request.args.get('monthly_payment')
    total_payment = request.args.get('total_payment')
    payments = json.loads(request.args.get('payments'))

    return render_template('results.html', amount=amount, duration=duration, rate=rate, monthly_payment=monthly_payment,
                           total_payment=total_payment, payments=payments)


if __name__ == '__main__':
    app.run(debug=True)
