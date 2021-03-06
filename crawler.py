from url_crawl import extract_article_urls
from parser import parse_article  
from interact_db import open_db, close_db, next_id, insert_into, select_from, column_name, TABLE_SECTIONS, TABLE_HEADLINES, TABLE_ARTICLES

def main():
    open_db()

    section_cols = column_name(TABLE_SECTIONS)
    sections = select_from(TABLE_SECTIONS)

    headline_cols = column_name(TABLE_HEADLINES)
    article_cols = column_name(TABLE_ARTICLES)

    next_article_id = next_id(TABLE_ARTICLES)

    for (section_id, section_name, base_url) in sections:
        print(section_id, base_url)
        article_urls = extract_article_urls(base_url)
        i = 0 
        print(article_urls[:3])
        for url in article_urls:
            data = parse_article(url)
            # parsing success
            if data != None: 
                headline = filter_dict_with_tuple(headline_cols, data)
                headline['section_id'] = section_id
                headline['article_id'] = next_article_id
                headline['cached'] = 1
                article = filter_dict_with_tuple(article_cols, data)
                # TODO photos processing
                insert_into(TABLE_ARTICLES, article)
                next_article_id += 1
            # parsing fail
            else:
                headline = filter_dict_with_tuple(headline_cols, {})
                headline['section_id'] = section_id
                headline['cached'] = 0
                headline['article_url'] = url
            
            insert_into(TABLE_HEADLINES, headline)

            i += 1
            if i >= 3:
                break

    close_db()

def filter_dict_with_tuple(key_tuple, dict_data):
    result = {}
    for key in key_tuple:
        result[key] = dict_data.get(key)
    return result

if __name__ == '__main__':
    main()
