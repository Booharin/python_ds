import numpy as np
import pandas as pd

# Topic 1

# 1
a = np.array([[1, 2, 3, 3, 1],
              [6, 8, 11, 10, 7]])
a.transpose()
mean_a = a.mean(axis=1)
print(mean_a)

# 2
a_centered = (a - mean_a[:, None]).transpose()
print(a_centered)

# 3
a_centered_sp = a_centered[:, 0].dot(a_centered[:, 1])
# число наблюдений 2
x = a_centered_sp / (2 - 1)
print(x)

# 4
print(np.cov(a)[0, 1])
print("---------------------------------")

# Topic 2

# 1
authors = pd.DataFrame({
    "author_id": [1, 2, 3],
    "author_name": ['Тургенев', 'Чехов', 'Островский']
})

authors = pd.DataFrame(authors)

book = pd.DataFrame({
    "author_id": [
        1,
        1,
        1,
        2,
        2,
        3,
        3
    ],
    "book_title": [
        'Отцы и дети',
        'Рудин',
        'Дворянское гнездо',
        'Толстый и тонкий',
        'Дама с собачкой',
        'Гроза',
        'Таланты и поклонники'
    ],
    "price": [
        450,
        300,
        350,
        500,
        450,
        370,
        290
    ]
})

print(book)
print("---------------------------------")

# 2
authors_price = pd.merge(authors, book, on='author_id', how='outer')

# 3
top5 = authors_price.nlargest(5, "price")
print(top5)
print("---------------------------------")

# 4
authors_stat = pd.DataFrame({
    "author_name": authors_price["author_name"],
    "min_price": authors_price["price"].min(),
    "max_price": authors_price["price"].max(),
    "mean_price": authors_price["price"].mean().astype(int)
})
print(authors_stat)
print("---------------------------------")

# 5
cover = pd.DataFrame(
    {'cover': ['твердая', 'мягкая', 'мягкая', 'твердая', 'твердая', 'мягкая', 'мягкая']}
)

authors_price = pd.concat([authors_price, cover], axis=1)
print(authors_price)
print("---------------------------------")

book_info = pd.pivot_table(authors_price,
                           values=['price'],
                           index=['author_name'],
                           columns=['cover'],
                           aggfunc=np.sum,
                           fill_value=0)
print(book_info)

book_info.to_pickle("book_info.pkl")
book_info2 = pd.read_pickle("book_info.pkl")
print("---------------------------------")

print(book_info.equals(book_info2))