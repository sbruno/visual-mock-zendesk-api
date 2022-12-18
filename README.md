

Known differences:
subject is not null, it is set to a string when left empty.
description is a legacy concept (setting a description creates a first comment) so is not implemented
There is one hardcoded admin, we don't look at the admin credentials provided and instead just use to a single default admin account.

Tried to cover the corner cases when post author_id is missing, it's likely covered import_many but hasn't been tested for update_many

Documentation says add_tags and remove_tags can only be done for the ids=? syntax for update_many, but in my experience it does work on the other syntax.




