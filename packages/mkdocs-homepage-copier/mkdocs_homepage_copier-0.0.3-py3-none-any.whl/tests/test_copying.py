import os
import shutil

from mkdocs.config.defaults import MkDocsConfig

from copier import HomepageCopier


def clean_up(temp_dir):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def test_homepage_copy_true():
    temp_dir = os.path.join("tests", "test_homepage_copy_true")
    src_file = "README.md"
    dest_file = os.path.join(temp_dir, "index.md")
    copier = HomepageCopier()
    config = MkDocsConfig()

    copier.config["copy"] = True
    copier.config["src"] = src_file
    copier.config["dest"] = dest_file

    clean_up(temp_dir)
    os.makedirs(temp_dir)

    _ = copier.on_config(config)
    assert os.path.exists(os.path.join(dest_file))

    copier.on_post_build(config)
    assert not os.path.exists(os.path.join(dest_file))

    clean_up(temp_dir)


def test_homepage_copy_false():
    temp_dir = os.path.join("tests", "test_homepage_copy_false")
    src_file = "README.md"
    dest_file = os.path.join(temp_dir, "index.md")
    copier = HomepageCopier()
    config = MkDocsConfig()

    copier.config["copy"] = False
    copier.config["src"] = src_file
    copier.config["dest"] = dest_file

    clean_up(temp_dir)
    os.makedirs(temp_dir)

    _ = copier.on_config(config)
    assert not os.path.exists(os.path.join(dest_file))

    clean_up(temp_dir)
