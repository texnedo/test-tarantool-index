box.cfg {listen=3301}

box.schema.sequence.create('test_seq', {min=1, start=1})

s1 = box.schema.space.create('test_hash')
s1:format(
        {
              {name = 'id', type = 'string'},
              {name = 'index', type = 'unsigned'},
              {name = 'band_name', type = 'string'},
              {name = 'year', type = 'unsigned'}
        }
)
s1:create_index('primary',
        {
              type = 'hash',
              parts = {'id'}
        }
)

s2 = box.schema.space.create('test_tree')
s2:format(
        {
              {name = 'id', type = 'string'},
              {name = 'index', type = 'unsigned'},
              {name = 'band_name', type = 'string'},
              {name = 'year', type = 'unsigned'}
        }
)
s2:create_index('primary',
        {
              type = 'tree',
              parts = {'id'}
        }
)
