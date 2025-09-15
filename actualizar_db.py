import sqlite3

conn = sqlite3.connect('horai.db')
cursor = conn.cursor()

# Verificar registros sin sesion_id
cursor.execute('SELECT COUNT(*) FROM conversaciones WHERE sesion_id IS NULL OR sesion_id = ""')
count = cursor.fetchone()[0]
print(f'Registros sin sesion_id: {count}')

# Actualizar registros existentes con un sesion_id por defecto
cursor.execute('UPDATE conversaciones SET sesion_id = "legacy-session-001" WHERE sesion_id IS NULL OR sesion_id = ""')
conn.commit()

print('Registros actualizados exitosamente')

# Verificar que se actualizó
cursor.execute('SELECT id, sesion_id, mensaje_usuario FROM conversaciones')
for row in cursor.fetchall():
    print(f'ID: {row[0]}, Sesión: {row[1]}, Mensaje: {row[2]}')

conn.close()