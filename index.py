from flask import Flask, render_template, request, g, redirect
import sqlite3

app = Flask(__name__)
database = "datafile.db"

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = sqlite3.connect(database)
        return g.sqlite_db

@app.teardown_appcontext
def close_connection(exception):
    print("我們正在關閉sql connection....")
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cash")
def cash_from():
    return render_template("cash.html")

@app.route("/cash", methods=["POST"])
def submit_cash():
    # 取得金額跟資料
    taiwanese_dollars = 0
    us_dollars = 0
    if request.values["taiwanese-dollars"] != "":
        taiwanese_dollars = request.values["taiwanese-dollars"]
    if request.values["us-dollars"] != "":
        us_dollars = request.values["us-dollars"]
    note = request.values["note"]
    date = request.values["date"]

    # 更新數據資料庫
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""insert into cash (taiwanese_dollars, us_dollars, note, date_info) values (?, ?, ?, ?)""",
                    (taiwanese_dollars,us_dollars, note, date))
    conn.commit()
    # 將使用者導回主頁面
    return redirect("/")

@app.route("/stock")
def stock_from():
    return render_template("stock.html")

if __name__ == "__main__":
    app.run(debug=True)
