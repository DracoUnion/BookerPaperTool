# -*- coding: utf-8 -*-
"""BookerPaperTool 冒烟测试：验证子命令注册、模块导入与输入校验。

不访问网络与大模型，可离线运行：python -m pytest 或 python -m unittest。
"""

import unittest
from argparse import Namespace

import BookerPaperTool
from BookerPaperTool import __main__ as main_mod
from BookerPaperTool import textbook, textbook_any, code, auto_research
from BookerPaperTool import openai as oai


def _build_parser():
    """按 __main__.main 的方式构建解析器，但不解析 sys.argv。"""
    import argparse
    parser = argparse.ArgumentParser(prog="BookerPaperTool")
    parser.add_argument("-D", "--debug", action="store_true", help="调试模式")
    subparsers = parser.add_subparsers()
    textbook.reg_subparser(subparsers)
    textbook_any.reg_subparser(subparsers)
    code.reg_subparser(subparsers)
    auto_research.reg_subparser(subparsers)
    return parser


class TestSubcommands(unittest.TestCase):
    def test_version_string(self):
        self.assertRegex(BookerPaperTool.__version__, r"^\d{4}\.\d+\.\d+\.\d+$")

    def test_subcommands_registered(self):
        parser = _build_parser()
        names = set(parser._subparsers._group_actions[0].choices)
        self.assertEqual(names, {"textbook", "textbook-any", "code", "auto-research"})

    def test_textbook_args(self):
        args = _build_parser().parse_args(
            ["-D", "textbook", "papers", "-t", "4", "-c", "2"])
        self.assertEqual(args.dir, "papers")
        self.assertEqual(args.threads, 4)
        self.assertEqual(args.check, 2)
        self.assertTrue(args.debug)

    def test_textbook_any_args(self):
        args = _build_parser().parse_args(["-D", "textbook-any", "materials"])
        self.assertEqual(args.dir, "materials")
        self.assertTrue(args.debug)

    def test_code_args(self):
        args = _build_parser().parse_args(
            ["code", "arxiv:2401.00001", "-o", "outdir"])
        self.assertEqual(args.fname, "arxiv:2401.00001")
        self.assertEqual(args.out, "outdir")

    def test_auto_research_args(self):
        args = _build_parser().parse_args(
            ["auto-research", "-p", "proj", "-g", "goal", "-ms", "10", "-y"])
        self.assertEqual(args.project, "proj")
        self.assertEqual(args.goal, "goal")
        self.assertEqual(args.max_steps, 10)
        self.assertTrue(args.yes)


class TestModuleApi(unittest.TestCase):
    def test_openai_public_api(self):
        for name in [
            "request_retry", "get_msgs_text", "repl_ins_token", "ensure_utf8",
            "dispatch_tools", "OpenAIClient", "base_schema", "func_schema",
            "params_schema", "model_schema", "model_list_schema",
            "str_list_schema", "str_str_map_schema", "ToolsMixin",
        ]:
            self.assertTrue(hasattr(oai, name), name)

    def test_entry_symbols(self):
        pairs = [
            (textbook, ["TextbookOrchestrator", "TextbookAgent", "textbook", "reg_subparser"]),
            (textbook_any, ["Any2TextbookOrchestrator", "Any2TextbookTools", "textbook_any", "reg_subparser"]),
            (code, ["CodeOrchestrator", "CodeAgent", "code", "reg_subparser"]),
            (auto_research, ["AutoResearchOrchestrator", "AutoResearchTools", "auto_research_handle", "reg_subparser"]),
        ]
        for mod, names in pairs:
            for name in names:
                self.assertTrue(hasattr(mod, name), f"{mod.__name__}.{name}")


class TestOrchestratorInit(unittest.TestCase):
    def _llm_args(self, **kw):
        base = dict(
            model="m", key="k", retry=1, temp=1.0, top_p=None,
            frequency_penalty=None, presence_penalty=None, max_tokens=None,
            host=None, user_agent="ua", no_stream=True, extra_body=None,
            conn_timeout=60, read_timeout=120, repetition_regex="",
            no_think=False, vmodel="", tti_model="", emb="",
        )
        base.update(kw)
        return Namespace(**base)

    def test_textbook_pj_dir(self):
        args = self._llm_args(dir="./__test_textbook_papers", threads=4, check=1, debug=False)
        o = textbook.TextbookOrchestrator(args)
        self.assertTrue(o.pj_dir.endswith("_textbook"))

    def test_auto_research_pj_dir(self):
        args = self._llm_args(project="./__test_auto_research", goal="", yes=False, debug=False)
        o = auto_research.AutoResearchOrchestrator(args)
        self.assertTrue(o.pj_dir.endswith("__test_auto_research"))


if __name__ == "__main__":
    unittest.main()
