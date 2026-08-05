import shutil, sqlite3, os, sys
DB = r"C:\Users\Younes\Desktop\AetherAI\bots\telegram_bot\database\users.db"
backup = DB + ".backup"
print('DB path:', DB)
# ensure DB exists
if not os.path.exists(DB):
    print('ERROR: DB file does not exist:', DB)
    sys.exit(2)
# create backup
shutil.copy2(DB, backup)
print('Backup created at', backup)
# check if searches column exists
conn = sqlite3.connect(DB)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(usage)")
cols = [row[1] for row in cursor.fetchall()]
print('usage table columns:', cols)
if 'searches' in cols:
    print('searches column already exists — no migration needed')
else:
    print('searches column missing — adding column')
    cursor.execute("ALTER TABLE usage ADD COLUMN searches INTEGER DEFAULT 0")
    conn.commit()
    # verify
    cursor.execute("PRAGMA table_info(usage)")
    cols2 = [row[1] for row in cursor.fetchall()]
    print('usage table columns after change:', cols2)
conn.close()
