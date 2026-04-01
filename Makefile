FULL_DEBUG = '$$\#FULL_DEBUG'

%.z5: %.inf Makefile
	inform -s -E1 $(if $(NODEBUG),,-D) -S $<

%.play: %.z5
	# frotz $<
	killall Gargoyle || echo "not running"
	open -a Gargoyle $<

.PHONY: html
html:
	pandoc -T "Our Lady of Thorns" -H html/styles.html -s docs/puzzles.md > html/puzzles.html
	pandoc -T "Our Lady of Thorns" -H html/styles.html -s docs/plot.md > html/plot.html
	pandoc -T "Our Lady of Thorns" -H html/styles.html -s docs/style.md > html/style.html
	pandoc -T "Our Lady of Thorns" -H html/styles.html -s docs/help.md > html/index.html
	cp walkthrough.txt html
	tail +8 thorns.scr |  awk -f scripts/tidy.awk | python3 scripts/transcript_to_html.py > html/final.html
	inform -E1 -S thorns.inf
	cp thorns.z5 html/

surge: html
	cd html && netlify deploy -p -d .
	open https://lady-of-thorns.netlify.app/
	rm thorns.z5

abbrevs:
	rm -f gametext.txt
	inform -r '$$TRANSCRIPT_FORMAT=1' -v5 thorns.inf
	 ../zabbrev/zabbrev-osx -n 95 -x3 -v5 thorns.inf > abbrevs-z5.inf
	rm gametext.txt

test:
	@clear; \
	output=$$(inform -E1 $(FULL_DEBUG) -D -S thorns.inf 2>&1); \
	stat=$$?; \
	if [ $$stat -ne 0 ] || echo "$$output" | grep -q "Warning"; then \
		echo "$$output"; \
		echo ""; \
		first_issue=$$(echo "$$output" | grep -E "(Error|Warning):" | head -1 | sed -E 's/^([^(]+)\(([0-9]+)\).*/\1:\2/'); \
		if [ -n "$$first_issue" ]; then \
			code -g "$$first_issue"; \
		fi; \
	else \
		frotz_ctrlc thorns.z5; \
	fi

.PHONY: walkthrough
walkthrough:
	cat walkthrough/1[a-z]-*.txt > walkthrough/1-start.txt
	cat walkthrough/2[a-z]-*.txt > walkthrough/2-initial-investigate.txt
	cat walkthrough/3[a-z]-*.txt > walkthrough/3-puzzles-east.txt
	cat walkthrough/4[a-z]-*.txt > walkthrough/4-upper.txt
	cat walkthrough/5[a-z]-*.txt > walkthrough/5-crypts.txt
	cat walkthrough/6[a-z]-*.txt > walkthrough/6-belltower-solar.txt
	cat walkthrough/7[a-z]-*.txt > walkthrough/7-undercroft.txt
	cat walkthrough/8[a-z]-*.txt > walkthrough/8-endings.txt
	cd walkthrough && cat 1-* 2-* 3-* 4-* 5-* 6-* 7-* > 17-combo.txt
	cd walkthrough && cat 1-* 2-* 3-* 4-* 5-* 6-* 7-* 8-* > 18-combo.txt
	cat walkthrough/18-combo.txt \
	| fgrep -v 'GOCHECK' \
	> walkthrough.txt
	cp walkthrough.txt walkthrough.rec

	cat alts/1[a-z]-*.txt > alts/1-start.txt
	cat alts/2[a-z]-*.txt > alts/2-initial-investigate.txt
	cat alts/3[a-z]-*.txt > alts/3-puzzles-east.txt
	cat alts/4[a-z]-*.txt > alts/4-upper.txt
	cat alts/5[a-z]-*.txt > alts/5-crypts.txt
	cat alts/6[a-z]-*.txt > alts/6-belltower-solar.txt
	cat alts/7[a-z]-*.txt > alts/7-undercroft.txt
	cat alts/8[a-z]-*.txt > alts/8-endings.txt
	cd alts && cat 1-* 2-* 3-* 4-* 5-* 6-* 7-* > 17-combo.txt
	cd alts && cat 1-* 2-* 3-* 4-* 5-* 6-* 7-* 8-* > 18-combo.txt
	cat alts/18-combo.txt \
	| fgrep -v 'GOTO' \
	> alts/walkthrough.txt
	cp alts/walkthrough.txt alts/walkthrough.rec


.PHONY: playtest
playtest:
	rm -f final.txt
	inform -E1 -D -S thorns.inf
	open -a Spatterlight thorns.z5

check-hints:
	@ggrep -oP '(?<=^Option )\w+' game_hints.inf | while read id; do \
		ggrep -qi "$$id" thorns.inf || echo "Not found: $$id"; \
	done

unit: walkthrough
	rm -f thorns.scr /tmp/diff
	output=$$(inform -E1 -D -S thorns.inf 2>&1); \
	stat=$$?; \
	if [ $$stat -ne 0 ] || echo "$$output" | grep -q "Warning"; then \
		echo "$$output"; \
		echo ""; \
		first_issue=$$(echo "$$output" | grep -E "(Error|Warning):" | head -1 | sed -E 's/^([^(]+)\(([0-9]+)\).*/\1:\2/'); \
		if [ -n "$$first_issue" ]; then \
			code -g "$$first_issue"; \
		fi; \
	else \
		echo "\nREPLAY\nwalkthrough\n" | dfrotz -S1000 -m -p thorns.z5; \
		awk -f scripts/test.awk thorns.scr && diff -N -u3 --color=always unit-walkthrough.scr thorns.scr > /tmp/diff ; \
		[ -s /tmp/diff ] && less -R /tmp/diff \
		&& read -r -p "Bless this output? [y/N] " reply && [[ "$$reply" == [yY] ]] && cp thorns.scr unit-walkthrough.scr \
		|| true ; \
	fi

alts: walkthrough
	rm -f thorns.scr
	output=$$(inform -E1 -D -S thorns.inf 2>&1); \
	stat=$$?; \
	if [ $$stat -ne 0 ] || echo "$$output" | grep -q "Warning"; then \
		echo "$$output"; \
		echo ""; \
		first_issue=$$(echo "$$output" | grep -E "(Error|Warning):" | head -1 | sed -E 's/^([^(]+)\(([0-9]+)\).*/\1:\2/'); \
		if [ -n "$$first_issue" ]; then \
			code -g "$$first_issue"; \
		fi; \
	else \
		echo "\nREPLAY\nalts/walkthrough\n" | dfrotz -S1000 -m -p thorns.z5; \
		awk -f scripts/test.awk thorns.scr && diff -N -u3 --color=always alts/unit-walkthrough.scr thorns.scr > /tmp/diff ; \
		[ -s /tmp/diff ] && less -R /tmp/diff \
		&& read -r -p "Bless this alt output? [y/N] " reply && [[ "$$reply" == [yY] ]] && cp thorns.scr alts/unit-walkthrough.scr \
		|| true ; \
	fi

clean:
	rm -f just_hints.z5 thorns.z3 thorns.z5 walkthrough.rec walkthrough.txt thorns.scr
	cd html && rm -f final.html plans.html plot.html puzzles.html style.html thorns.z5 walkthrough.txt

apple2: thorns.z3
	rm /tmp/thorns_apple2.dsk
	/Users/joel/if/interlz/interlz3 /Users/joel/if/interlz/info3m.bin thorns.z3 /tmp/thorns_apple2.dsk
	open /tmp/thorns_apple2.dsk
