from functools import wraps
from flask import session, redirect, url_for, flash, request

adm = 2
usuario = 1

def permitirAcesso(necessario):

    def decorator(f):
        @wraps(f)
        def decorador(*args, **kwargs):
          
            if 'logado' not in session or session['logado'] != True:
                flash('Você precisa fazer login para acessar esta página!', 'danger')
                return redirect(url_for('login')) 

            nivel = session.get('prioridade', 0) 

            if nivel < necessario:
               
                flash('Você não tem permissão para acessar esta página.', 'warning')
                
           
                if nivel == usuario:
                    return redirect(url_for('voosDisponiveis'))
                elif nivel != usuario and nivel != adm:
                    return redirect(url_for('login'))
                
          
            return f(*args, **kwargs)
        return decorador
    return decorator