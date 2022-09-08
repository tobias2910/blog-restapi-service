"""adjusted the image_url field in the projects table

Revision ID: c8b1eede9fc1
Revises: d18253d5cdec
Create Date: 2022-08-27 00:06:00.625026

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c8b1eede9fc1"
down_revision = "d18253d5cdec"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_articles_author", table_name="articles")
    op.drop_index("ix_articles_id", table_name="articles")
    op.drop_table("articles")
    op.drop_index("ix_user_email", table_name="user")
    op.drop_index("ix_user_id", table_name="user")
    op.drop_table("user")
    op.drop_index("ix_skill_levels_id", table_name="skill_levels")
    op.drop_index("ix_skill_levels_level", table_name="skill_levels")
    op.drop_table("skill_levels")
    op.drop_index("ix_projects_id", table_name="projects")
    op.drop_table("projects")
    op.drop_index("ix_skills_id", table_name="skills")
    op.drop_index("ix_skills_name", table_name="skills")
    op.drop_table("skills")
    op.drop_index("ix_categories_category", table_name="categories")
    op.drop_index("ix_categories_description", table_name="categories")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('categories_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("category", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="categories_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_categories_id", "categories", ["id"], unique=False)
    op.create_index("ix_categories_description", "categories", ["description"], unique=False)
    op.create_index("ix_categories_category", "categories", ["category"], unique=False)
    op.create_table(
        "skills",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("category_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("skill_level_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], name="skills_category_id_fkey"),
        sa.ForeignKeyConstraint(["skill_level_id"], ["skill_levels.id"], name="skills_skill_level_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="skills_pkey"),
    )
    op.create_index("ix_skills_name", "skills", ["name"], unique=False)
    op.create_index("ix_skills_id", "skills", ["id"], unique=False)
    op.create_table(
        "projects",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("imageUrl", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("project_url", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("tags", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="projects_pkey"),
    )
    op.create_index("ix_projects_id", "projects", ["id"], unique=False)
    op.create_table(
        "skill_levels",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("level", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="skill_levels_pkey"),
    )
    op.create_index("ix_skill_levels_level", "skill_levels", ["level"], unique=False)
    op.create_index("ix_skill_levels_id", "skill_levels", ["id"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("password", sa.TEXT(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
    )
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    op.create_index("ix_user_email", "user", ["email"], unique=False)
    op.create_table(
        "articles",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("author", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("image_url", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("content", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("tags", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("created_at", sa.DATE(), autoincrement=False, nullable=False),
        sa.Column("updated_at", sa.DATE(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="articles_pkey"),
    )
    op.create_index("ix_articles_id", "articles", ["id"], unique=False)
    op.create_index("ix_articles_author", "articles", ["author"], unique=False)
    # ### end Alembic commands ###
