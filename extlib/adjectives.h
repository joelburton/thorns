
#Ifv5;
Property adj_name;
Property noun_name;
#Ifnot;
Property individual adj_name;
Property individual noun_name;
#Endif;

#Ifv5;
[MatchNameList p_obj p_prop _w _matched _an _count _i;
	_an = p_obj.&p_prop;
	if(_an == 0) { wn++; return 0; }
	_count = p_obj.#p_prop;
	@log_shift _count (-1) -> _count; ! Divide by 2
	while(true) {
		_w = NextWord();
		@scan_table _w _an _count -> _i ?_MNL_match;
		return _matched;
._MNL_match;
		_matched++;
	}
];
#Ifnot;
[MatchNameList p_obj p_prop _w _matched _base _an _count _i;
	_an = p_obj.&p_prop;
	if(_an == 0) { wn++; return 0; }
	_count = p_obj.#p_prop / 2;
	while(true) {
		_w = NextWord();
		_base = _matched;
		for(_i = 0 : _i < _count : _i++)
			if(_w == _an-->_i) { _matched++; break; }
		if(_matched == _base) return _matched;
	}
];
#Endif;

Class AdjObject
	with
		parse_name [ _adj _noun;
			_adj = MatchNameList(self, adj_name);
			wn--;
			_noun = MatchNameList(self, noun_name);
			if(_noun) return _noun + _adj;
		];
