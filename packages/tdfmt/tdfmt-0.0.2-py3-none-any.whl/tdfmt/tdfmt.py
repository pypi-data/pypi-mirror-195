from datetime import timedelta
# "inspired" by https://github.com/golang/go/blob/master/src/time/time.go

# tdfmt returns a string representing the timedelta in the form "72h3m0.5s".
# Leading zero units are omitted. As a special case, durations less than one second format 
# use a smaller unit (milli-, or microseconds) to ensure that the leading digit is non-zero.
def tdfmt(td: timedelta) -> str:
	MILLISECOND = 1000
	SECOND = 1000*MILLISECOND
	DAY = 24*3600

	# Longest output is "-10000000000h00m00.000001s" (26 chars).
	buf = bytearray([0]*32)
	w = len(buf)

	u = td.days*DAY + td.seconds*SECOND + td.microseconds
	neg = u < 0
	if neg:
		u = -u

	if u < SECOND:
		w -= 1
		buf[w] = ord("s")
		if u < MILLISECOND:
			prec = 0
			w -= 2
			buf[w:w+2] = bytes("µ", encoding="utf-8")
		else:
			prec = 3
			w -= 1
			buf[w] = ord("m")
		w, u = fracfmt(buf, w, u, prec)
		w = intfmt(buf, w, u)
	else:
		w -= 1
		buf[w] = ord("s")
		w, u = fracfmt(buf, w, u, 6)
		w = intfmt(buf, w, u%60)
		u //= 60
		if u > 0:
			w -= 1
			buf[w] = ord("m")
			w = intfmt(buf, w, u%60)
			u //= 60
			if u > 0:
				w -= 1
				buf[w] = ord("h")
				w = intfmt(buf, w, u)

	if neg:
		w -= 1
		buf[w] = ord("-")

	return buf[w:].decode()

# fracfmt formats the fraction of v/10**prec (e.g., ".12345") into the
# tail of buf, omitting trailing zeros. It omits the decimal
# point too when the fraction is 0. It returns the index where the
# output bytes begin and the value v/10**prec.
def fracfmt(buf: bytearray, w: int, v: int, prec: int) -> (int, int):
	# Omit trailing zeros up to and including decimal point.
	write = False
	for i in range(prec):
		digit = v%10
		write = write or digit != 0
		if write:
			w -= 1
			buf[w] = ord("0") + digit
		v //= 10
	if write:
		w -= 1
		buf[w] = ord(".")
	return w, v

# intfmt formats v into the tail of buf.
# It returns the index where the output begins.
def intfmt(buf: bytearray, w: int, v: int) -> (int, int):
	if v == 0:
		w -= 1
		buf[w] = ord("0")
	else:
		while v > 0:
			w -= 1
			buf[w] = ord("0") + v%10
			v //= 10
	return w
