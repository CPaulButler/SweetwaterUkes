import argparse
import functools
import http.server
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and serve the local site folder for testing."
    )
    parser.add_argument(
        "--dir",
        default="site",
        help="Directory to serve (default: site)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind (default: 8000)",
    )
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        help="Bind address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the site directory before rebuilding",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip rebuilding the site before serving",
    )
    return parser.parse_args()


class NoCacheRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def build_site(repo_root: Path, site_dir: Path, clean: bool) -> int:
    if clean and site_dir.exists():
        shutil.rmtree(site_dir)

    site_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_root / "music", site_dir / "music", dirs_exist_ok=True)
    shutil.copytree(repo_root / "assets", site_dir / "assets", dirs_exist_ok=True)
    shutil.copy2(repo_root / "favicon.svg", site_dir / "favicon.svg")

    genlist_path = shutil.which("genlist")
    if not genlist_path:
        print(
            "genlist not found. Install with: pipx install genlist-butler",
            file=sys.stderr,
        )
        return 1

    index_path = site_dir / "index.html"
    subprocess.run(
        [genlist_path, "music", str(index_path), "--no-intro"],
        check=True,
        cwd=str(repo_root),
    )
    (site_dir / ".nojekyll").touch()
    return 0


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    site_dir = (repo_root / args.dir).resolve()

    if not args.skip_build:
        try:
            result = build_site(repo_root, site_dir, args.clean)
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Build failed: {exc}", file=sys.stderr)
            return 1
        if result != 0:
            return result

    if not site_dir.exists():
        print(f"Directory not found: {site_dir}", file=sys.stderr)
        return 1

    handler = functools.partial(NoCacheRequestHandler, directory=str(site_dir))
    server = http.server.ThreadingHTTPServer((args.bind, args.port), handler)

    url = f"http://{args.bind}:{args.port}/"
    print(f"Serving {site_dir}")
    print(f"Open {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
        return 0
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
