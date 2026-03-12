/^> REPLAY$/ { skip=1; next }
skip && /^\s*$/ { skip=0; next }
skip { next }
{ print }
