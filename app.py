from flask import Flask, render_template, send_file
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)

engine = create_engine('sqlite:///books.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
current_directory = os.path.dirname(__file__)
pdf_folder = os.path.join(current_directory, 'static')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    creator = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    image_url = Column(String(100))

    def __repr__(self):
        return f"<Book {self.id}: {self.title}>"


Base.metadata.create_all(engine)

book_data = [
    {"title": "Пригоди Шерлока Холмса", "creator": "Артур Конан Дойль", "description": "Пригоди Шерлока Холмса - серія детективних оповідань, у яких головним героєм є знаменитий детектив Шерлок Холмс, що розслідує різні загадкові злочини в Лондоні кінця XIX століття.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/i/m/img383_1_43.jpg"},
    {"title": "Дракула", "creator": "Брэм Стокер", "description": "Дракула - роман жахів, який розповідає про вампіра на ім'я Дракула і його вплив на життя мешканців Лондона. Це класичне твір вважається одним із найвідоміших у світовій літературі та суттєво вплинув на жанр жахів.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/i/s/isbn_978_617_7914_61_6_0.jpg"},
    {"title": "Код Да Вінчі", "creator": "Ден Браун", "description": "Код Да Вінчі - трилер, у якому розслідується загадкове вбивство і водночас розкриваються таємниці, пов'язані з таємними товариствами, мистецтвом та релігією. Роман прославився своїми заплутаними загадками і непередбачуваним сюжетом.", "image_url": "https://upload.wikimedia.org/wikipedia/uk/7/72/Da_vinci_code.jpg"},
    {"title": "ТРИ ТОВАРИЩА", "creator": "Еріх Марія Ремарк", "description": "ТРИ ТОВАРИЩА - роман, що описує життя трьох друзів в Німеччині в період після Першої світової війни. Книга торкається тем дружби, кохання, втрати та надії в складні історичні часи.", "image_url": "https://content.rozetka.com.ua/goods/images/big/262035943.jpg"},
    {"title": "Гаррі Поттер і філософський камінь", "creator": "Джоан Роулінг", "description": "Гаррі Поттер і філософський камінь - це перша книга з сірії про юного чарівника Гаррі Поттера, написана Джоан Роулінг. У цій книзі Гаррі дізнається про своє справжнє походження та вступає до Хогвартсу, школи чарівництва і чаклунства.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/4/1/41_1_131.jpg"},
    {"title": "Дванадцять стільців", "creator": "Ілья Ільф, Євген Петров", "description": "Дванадцять стільців - роман-фельетон, у якому описуються пригоди молодої людини у пошуках втраченого спадку. Книга прославилася своїми яскравими персонажами та гумором.", "image_url": "https://readukrainianbooks.com/uploads/posts/books/2/8/8/3/zolote-telja-yevgen-petrovich-petrov.jpg"},
    {"title": "Собаче серце", "creator": "Михайло Булгаков", "description": "Собаче серце - алегорична повість, в якій описується історія професора, який вживляє в людину собаче серце, що призводить до несподіваних наслідків та роздумів про людську природу.", "image_url": "https://static.yakaboo.ua/media/catalog/product/c/o/cover_468_7.jpg"},
    {"title": "Казки Пушкіна", "creator": "Олександр Пушкін", "description": "Казки Пушкіна - збірка казок російського поета", "image_url": "https://knygy.com.ua/pix/b3/e8/2b/b3e82bcc7fdeef9ca96c9b91addfc142.jpg"},
    {"title": "Граф Монте-Крісто", "creator": "Олександр Дюма", "description": "Граф Монте-Крісто - роман-пригода, що розповідає історію Едмонда Дантеса, який, опинившись невинно засудженим, вчиняє дивовижний втечу з в'язниці і починає мстити своїм образникам", "image_url": "https://lavkababuin.com/image/cachewebp/alias/graf-monte-kristo-570081/graf-monte-kristo-570081-main-1000x1000.webp"},
    {"title": "Двадцять тисяч льє під водою", "creator": "Жюль Верн", "description": "Двадцять тисяч льє під водою - це класичний науково-фантастичний роман, написаний французьким письменником Жюлем Верном та опублікований в 1870 році. Роман розповідає історію капітана Немо і його підводної акустичної човна Наутилус", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/i/m/img_11966.jpg"}
]


def init_db():
    session = Session()
    if session.query(Book).count() < 10:
        for data in book_data:
            bookr = Book(title=data["title"], creator=data["creator"], description=data["description"], image_url=data["image_url"])
            session.add(bookr)
        session.commit()


@app.route('/download_book/<int:book_id>')
def download_book(book_id):
    session = Session()
    book_datas = session.query(Book).filter_by(id=book_id).first()
    if book_datas:
        pdf_path = os.path.join(pdf_folder, f'{book_id}.pdf')
        if os.path.exists(pdf_path):
            try:
                return send_file(pdf_path, as_attachment=True)
            except Exception as e:
                return str(e)
        else:
            return "Файл не найден"
    else:
        return "Книга не найдена"


@app.route('/')
def index():
    session = Session()
    try:
        books = session.query(Book).all()
        return render_template('index.html', books=books)
    except Exception as e:
        return f"Ошибка при получении данных из базы данных: {e}"
    finally:
        session.close()


@app.route('/book/<int:book_id>')
def book(book_id):
    session = Session()
    try:
        book_dataa = session.query(Book).filter_by(id=book_id).first()
        if book_dataa:
            return render_template('book.html', book=book_dataa)
        else:
            return "Книга не найдена", 404
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
