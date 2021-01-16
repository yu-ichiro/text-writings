tmux使っている時だけ一部のANSIカラーが表示されていなかったたった1文字のミス
===

[status: published]
[url: https://zenn.dev/articles/3d82b4ddcd255e]


powerline/zshから脱却できていないせいでエラーメッセージがだんだん増えてきているのでそろそろなんの設定もカスタマイズもしない環境でトレーニングするべきかなと思い始めています。

# 本日の事件

通常のターミナル（Mac/iTerm2/TERM=xterm-256color/zsh）では問題なくANSI拡張カラーが表示できるのにtmuxに入ると正しく色がつかないという現象が起こっていた。

最初の段階では全体的に色が反映されていない感じだったが、こちらはここらへん（ https://github.com/tmux/tmux/issues/1246 ）を参考に直してとりあえず色がつくようになった。

*カーソル左のプロンプトだけ*

色はとりあえずつくのだが、三行のプロンプトを使っている（わかる煩わしいと思う自分でも）うちの一番下の左側にしか色がつかなかった。

# 解決

しばらくこの現象は見てみぬふりしていたんですが、powerlineを復活させてvimが綺麗に立ち上がるようになって嬉しくなったついでにこいつもどうにかしようと思って調査を始めました。

すぐに自前の関数で色を変更している部分が着色されていなくて、直でエスケープシーケンスを打っていた左下のプロンプトにだけ着色されていたことに気づきました。

しばらく試行錯誤していたのですが、ついに原因発見！

カラーコードの仕組みはここ(https://qiita.com/PruneMazui/items/8a023347772620025ad6#%E5%87%BA%E5%8A%9B%E8%89%B2%E3%81%AE%E5%A4%89%E6%9B%B4%E6%8B%A1%E5%BC%B5)が詳しいですが、大体
```
front_color=1  # 0~256の数字
back_color=15  # 0~256の数字
front=38;5;{color};
back=48;5;{color};
\e[${front}${back}m
```

このように`\e[`と`m`の間にセミコロン区切りのコードを入れていく形になっています。
そしてこの *セミコロン区切り* というところが今回は問題でした。

末端の区切り文字をどうするかっていうのはエンジニア界隈においては哲学的問題ですが（ファイルの末端は改行文字にした方がいい、辞書リテラルや配列リテラルの最後の項目のお尻にはカンマをつけるべきなど、、いずれも諸説あると思います）、今回の場合は上のコードのように実際のコードも組んでいたので実際に吐き出されるコードは

```
\e[38;5;1;48;5;15;m
```

のような形をしていました。メインで使っていたzsh君はなんの問題もなく正しく解釈してくれていたみたいです。
ただ、上の記事を読んでもらうとわかるのですが、mの前のセミコロンはどの例にも載っていないのでおそらくANSIの文法的には厳密には則していなかったみたいです。

なのでセパレータを入れる処理を横着せず、

```
front_color=1  # 0~256の数字
back_color=15  # 0~256の数字
front=38;5;{color}
back=48;5;{color}
[[ "$front" != "" && "$back" != "" ]]&&sep=";"
\e[${front}${sep}${back}m
```

のように書き直したところ、無事にtmuxでも全てのプロンプトが綺麗に映るようになりました。
普通のターミナルはそこらへん勝手にいい感じに解釈してくれてたみたいなので変なところで問題が起こっているケース、他にもありそうじゃないですか？？？　ないかー

# はしがき

やっぱりエラーを吐いてくれるプログラムとかって本当に親切です。目grepで問題箇所を探す能力って限界があるし、今回みたいにうまくいくのって毎回じゃないので、普段から仕様にそった綺麗なコードを心がけようと思いました。今日のはどうでもいい問題ですが、どうでもよくはない問題の根本がどうでもいい仕様の把握漏れとかよくある話ですし、、、