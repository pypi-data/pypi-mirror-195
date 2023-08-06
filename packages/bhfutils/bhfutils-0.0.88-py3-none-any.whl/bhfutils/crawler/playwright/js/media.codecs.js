/**
 * Input might look funky, we need to normalize it so e.g. whitespace isn't an issue for our spoofing.
 *
 * @example
 * video/webm; codecs="vp8, vorbis"
 * video/mp4; codecs="avc1.42E01E"
 * audio/x-m4a;
 * audio/ogg; codecs="vorbis"
 * @param {String} arg
 */
const parseInput = arg => {
    const [mime, codecStr] = arg.trim().split(';')
    let codecs = []
    if (codecStr && codecStr.includes('codecs="')) {
        codecs = codecStr
            .trim()
            .replace(`codecs="`, '')
            .replace(`"`, '')
            .trim()
            .split(',')
            .filter(x => !!x)
            .map(x => x.trim())
    }
    return {
        mime,
        codecStr,
        codecs
    }
}

const canPlayType = {
    // Intercept certain requests
    apply: function (target, ctx, args) {
        if (!args || !args.length) {
            return target.apply(ctx, args)
        }
        const {mime, codecs} = parseInput(args[0])
        if (mime === 'audio/ogg') {
            return ''
        }
        // This specific mp4 codec is missing in Chromium
        if (mime === 'audio/mpeg') {
            return 'maybe'
        }
        if (mime === 'audio/wav') {
            return ''
        }
        if (mime === 'audio/x-m4a' && !codecs.length) {
            return 'maybe'
        }
        if (mime === 'audio/aac' && !codecs.length) {
            return 'maybe'
        }

        if (mime === 'video/ogg') {
            return ''
        }
        if (mime === 'video/webm') {
            return ''
        }
        if (mime === 'video/mp4'  && !codecs.length) {
            return 'probably'
        }
        if (mime === 'video/x-matroska') {
            return ''
        }
        // Everything else as usual
        return target.apply(ctx, args)
    }
}

/* global HTMLMediaElement */
utils.replaceWithProxy(
    HTMLMediaElement.prototype,
    'canPlayType',
    canPlayType
)