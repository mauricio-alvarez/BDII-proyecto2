CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    submitter TEXT,
    authors TEXT,
    title TEXT,
    comments TEXT,
    journal_ref TEXT,
    doi TEXT,
    report_no TEXT,
    categories TEXT,
    license TEXT,
    abstract TEXT,
    update_date DATE
);

CREATE TABLE versions (
    id SERIAL PRIMARY KEY,
    article_id TEXT REFERENCES articles(id),
    version TEXT,
    created TIMESTAMP
);

CREATE TABLE authors_parsed (
    id SERIAL PRIMARY KEY,
    article_id TEXT REFERENCES articles(id),
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT
);

delete from articles;
delete from versions;
delete from authors_parsed;

select count(*) from articles;
