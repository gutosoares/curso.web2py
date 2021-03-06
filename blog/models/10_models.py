Blog = db.define_table('blog',
                       Field('title', notnull=True, unique=True),
                       Field('description', 'text'),
                       auth.signature
                       )

Category = db.define_table('category',
                           Field('name')
                           )

Post = db.define_table('post',
                       Field('blog', 'reference blog'),  # FK
                       Field('title', notnull=True),
                       Field('slug'),
                       Field('post_body', 'text'),
                       Field('is_draft', 'boolean'),
                       Field('tags', 'list:string'),
                       Field('category', 'list:reference category'),
                       auth.signature
                       )

