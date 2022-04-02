create table one_m_notes (
    note_id integer PRIMARY KEY autoincrement not null,
    --title TEXT,
    note TEXT
    );

create table one_m_tags (
    tag_id integer PRIMARY KEY autoincrement not null,
    tag TEXT
    );

create table  m_m_notes_tags(
    note_id INT,
    tag_id INT,
    PRIMARY KEY (note_id, tag_id) , -- explicit pk
    CONSTRAINT note_fk FOREIGN KEY(note_id) REFERENCES one_m_notes(note_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT tag_fk FOREIGN KEY(tag_id) REFERENCES one_m_tags(tag_id) ON UPDATE CASCADE ON DELETE CASCADE
    );