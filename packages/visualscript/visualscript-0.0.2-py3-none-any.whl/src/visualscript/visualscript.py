if __name__ == '__main__':
    import argparse
    from pathlib import Path
    import sys
    from PyQt5.QtWidgets import QApplication
    from editor.editor_window import EditorWindow

    parser = argparse.ArgumentParser(
        prog="VisualScript",
        description="Open scripts in visual scripting editor.",
        epilog="contact: adam.wachowicz@vp.pl")
    parser.add_argument("-f", "--paths", metavar="paths", nargs="+", help="paths to scripts you want to open")

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    wnd = EditorWindow()
    wnd.show()

    args = parser.parse_args()
    wnd.onFileOpen(args.file_paths)
    # for arg in args:
    #     print(arg)
        # path = Path(arg)
        # if path.is_file():
        #     wnd.


    sys.exit(app.exec_())