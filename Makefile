FULL_DEBUG = '$$\#FULL_DEBUG'

.PRECIOUS: %.z5 %.debug.z5 %.playtest.z5

define OPEN_OR_ERROR
	@rm -f $@
	@output=$$(inform -E1 $(1) $< /tmp/temp.z5 2>&1); \
	if echo "$$output" | grep -q ": Error:\|: Warning:"; then \
		first=$$(echo "$$output" | grep -m1 ": Error:\|: Warning:" | \
		sed 's/\(.*\)(\([0-9]*\)):.*/\1:\2/'); \
		echo "$$output"; \
		code --goto "$$first"; \
		exit 1; \
	else \
		mv /tmp/temp.z5 $@; \
		$(2); \
	fi
endef

%.z5: %.inf Makefile extlib/*
	$(call OPEN_OR_ERROR,,echo $@)

%.debug.z5: %.inf Makefile extlib/*
	$(call OPEN_OR_ERROR,-D $(FULL_DEBUG),echo $@)

%.playtest.z5: %.inf Makefile extlib/*
	$(call OPEN_OR_ERROR,-D,echo $@)


%.play: %.z5
	open -a Gargoyle $<

%.debug.play: %.debug.z5
	open -a Gargoyle $<

%.playtest.play: %.playtest.z5
	open -a Gargoyle $<


%.test: %.z5
	frotz_ctrlc $<

%.debug.test: %.debug.z5
	frotz_ctrlc $<

%.playtest.test: %.playtest.z5
	frotz_ctrlc $<


%.html: %.inf docs/*.md Makefile %.unit
	make $*.z5
	cp $*.z5 html/
	make $*.debug.z5
	cp $*.debug.z5 html/$*-debug.z5
	pygmentize -f html -O full -l inform6 thorns.inf > html/source.html
	pandoc -H source/styles.html -s docs/puzzles.md > html/puzzles.html
	pandoc -H source/styles.html -s docs/plot.md > html/plot.html
	pandoc -H source/styles.html -s docs/style.md > html/style.html
	pandoc -H source/styles.html -s docs/index.md > html/index.html
	cp unit/commands.rec html/walkthrough.txt
	tail +8 unit/current.scr |  awk -f scripts/tidy.awk \
		| python3 scripts/transcript_to_html.py > html/walkthrough.html
	cp source/{intro.pdf,thorns.jpg,play.html,styles.html,thorns.png} html/

%.abbrevs: %.inf Makefile
	rm -f gametext.txt
	inform -r '$$TRANSCRIPT_FORMAT=1' -v5 $<
	../zabbrev/zabbrev-osx -n 95 -x3 -v5 $< > $@.inf
	rm gametext.txt


%.upload: %.html
	cd html && netlify deploy -O -p -d .
	rm *.z5

define MAKE_TESTS
	cat $(1)/1[a-z]-*.txt > $(1)/1-start.txt
	cat $(1)/2[a-z]-*.txt > $(1)/2-initial-investigate.txt
	cat $(1)/3[a-z]-*.txt > $(1)/3-puzzles-east.txt
	cat $(1)/4[a-z]-*.txt > $(1)/4-upper.txt
	cat $(1)/5[a-z]-*.txt > $(1)/5-crypts.txt
	cat $(1)/6[a-z]-*.txt > $(1)/6-belltower-solar.txt
	cat $(1)/7[a-z]-*.txt > $(1)/7-undercroft.txt
	cat $(1)/8[a-z]-*.txt > $(1)/8-endings.txt
	cat $(1)/{1,2,3,4,5,6,7,8}-* > $(1)/18-combo.txt
	cat $(1)/18-combo.txt | fgrep -v 'GOCHECK' > $(1)/$(2)
	cp $(1)/$(2) $(1)/$(patsubst %.txt,%.rec,$(2))
endef

%.create-unit: Makefile unit/[0-9]*
	$(call MAKE_TESTS,unit,commands.txt)

%.create-alts: Makefile alts/[0-9]*
	$(call MAKE_TESTS,alts,commands.txt)

clean:
	fd -u ".*~" -x rm
	rm -f *.z5 *.scr
	rm -f html/*
	rm -f unit/[0-9][0-9]-combo* unit/[0-9]-* unit/current.*
	rm -f alts/[0-9][0-9]-combo* alts/[0-9]-* unit/current.*
	rm -f unit/commands.txt unit/commands.rec
	rm -f alts/commands.txt alts/commands.rec

%.hint-check: %.inf %-hints.inf Makefile
	@ggrep -oP '(?<=^Option )\w+' $< | while read id; do \
		ggrep -qi "$$id" $*.inf || echo "Not found: $$id"; \
	done


# run commands.rec through dfrotz, saving transcript to current.scr
# if there are differences:
#   - show diff current.scr <-> expected.scr
#   - on exiting diff, give them option to "bless"
#     (which copies current.scr to expected.scr)

define RUN_WALKTHROUGH
	rm -f $(2)/current.scr
	printf "$(2)/current.scr\nREPLAY\n$(2)/commands.rec\nn\n" \
		| dfrotz -S1000 -m -p $< ; \
	awk -f scripts/test.awk $(2)/current.scr; \
		diff -N -u3 --color=always $(2)/expected.scr $(2)/current.scr \
		> /tmp/diff ; \
	if [ -s /tmp/diff ]; then \
		less -R /tmp/diff; \
		read -r -p "Bless this output? [y/N] " reply; \
		if [ "$$reply" = "y" ] || [ "$$reply" = "Y" ]; then \
			cp $(2)/current.scr $(2)/expected.scr; \
		fi; \
	fi;
endef

%.unit: %.playtest.z5 %.create-unit
	$(call RUN_WALKTHROUGH,,unit)

%.alts: %.playtest.z5 %.create-alts
	$(call RUN_WALKTHROUGH,,alts)

