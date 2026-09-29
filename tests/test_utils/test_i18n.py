# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Noxfort Systems
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# File: tests/test_utils/test_i18n.py
# Description: Tests for the I18nManager utility.

import json
import pytest
from src.utils.i18n import I18nManager, backend_i18n


def test_i18n_flatten_dict():
    nested = {
        "menu": {
            "file": {
                "open": "Abrir",
                "save": "Salvar {name}"
            },
            "edit": "Editar"
        }
    }
    mgr = I18nManager.__new__(I18nManager)
    flat = mgr._flatten_dict(nested)
    assert flat["menu.file.open"] == "Abrir"
    assert flat["menu.file.save"] == "Salvar {name}"
    assert flat["menu.edit"] == "Editar"


def test_i18n_load_and_translate(tmp_path):
    locale_dir = tmp_path / "locale"
    locale_dir.mkdir()
    pt_file = locale_dir / "pt_BR.json"
    pt_file.write_text(json.dumps({
        "app": {
            "title": "SFusion",
            "greeting": "Olá, {user}!"
        }
    }), encoding="utf-8")

    mgr = I18nManager(locale_dir=str(locale_dir), language="pt_BR")
    assert mgr.t("app.title") == "SFusion"
    assert mgr.t("app.greeting", user="Gabriel") == "Olá, Gabriel!"
    # Missing key returns the key itself
    assert mgr.t("app.nonexistent") == "app.nonexistent"


def test_i18n_missing_file_and_invalid_json(tmp_path):
    locale_dir = tmp_path / "loc"
    locale_dir.mkdir()

    # Missing file
    mgr1 = I18nManager(locale_dir=str(locale_dir), language="nonexistent_lang")
    assert mgr1.t("any.key") == "any.key"

    # Malformed JSON
    bad_file = locale_dir / "bad.json"
    bad_file.write_text("not json", encoding="utf-8")
    mgr2 = I18nManager(locale_dir=str(locale_dir), language="bad")
    assert mgr2.t("any.key") == "any.key"


def test_backend_i18n_instance():
    # Verify global instance works
    assert backend_i18n.locale_dir == "locale_backend"
    assert backend_i18n.language == "pt_BR"
