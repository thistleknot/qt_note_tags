insert into one_m_notes (title, note) values ('first test','initial test notes');
insert into one_m_notes (title, note) values ('second test', 'more test notes');
insert into one_m_notes (title, note) values ('two tag test', 'this is an interesting test');

insert into one_m_tags (tag) values ('test');
insert into one_m_tags (tag) values ('interesting');

insert into m_m_notes_tags (note_id, tag_id) values (1,1);
insert into m_m_notes_tags (note_id, tag_id) values (2,2);
insert into m_m_notes_tags (note_id, tag_id) values (3,1);
insert into m_m_notes_tags (note_id, tag_id) values (3,2);

