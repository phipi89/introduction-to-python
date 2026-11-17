import numpy as np
import scipy.signal as sg
import scipy.io.wavfile as wav


class NoiseBandVocoder:
    """
    A cochlear-implant-style noise-band vocoder.

    At initialization, designs a logarithmically spaced band-pass filter bank,
    a low-pass filter for envelope extraction, per-band gains for optional
    high-frequency tilt, and a reproducible random generator.

    Processing:
    1) Filter input into bands.
    2) Extract Hilbert magnitude envelopes.
    3) Generate band-limited noise carriers.
    4) Multiply carriers by envelopes and high frequency tilt.
    5) Sum across bands and re-normalize.

    Parameters
    ----------
    sample_rate : int
        Sampling rate in Hz.
    n_bands : int
        Number of analysis/synthesis bands.
    min_freq : float
        Lower edge of the filter bank (Hz).
    max_freq : float
        Upper edge of the filter bank (Hz).
    envelope_lowpass : float
        Cutoff (Hz) of the envelope smoothing low-pass filter.
    high_freq_tilt : float
        dB/octave gain tilt applied to band outputs (0 disables).
        Positive values brighten the output by boosting higher bands.
    band_filter_order : int
        Order of Butterworth band-pass filters (even suggested).
    envelope_filter_order : int
        Order of Butterworth low-pass filter for envelopes.
    rng_seed : int or None
        Seed for reproducible noise carriers. None => nondeterministic.
    """

    def __init__(self,
                 sample_rate,
                 n_bands=12,
                 min_freq=200,
                 max_freq=8000,
                 envelope_lowpass=400,
                 high_freq_tilt=0,
                 band_filter_order=4,
                 envelope_filter_order=2
                 rng_seed=None):

        self.sample_rate = sample_rate
        self.n_bands = n_bands
        self.envelope_lowpass = envelope_lowpass
        self.high_freq_tilt = high_freq_tilt
        self.band_filter_order = band_filter_order
        self.envelope_filter_order = envelope_filter_order
        self._rng = numpy.random.default_rng(rng_seed)

        # Prepare filter bank
        self.band_edges = self.compute_band_edges(n_bands, min_freq, max_freq)
        self.band_centers = np.sqrt(self.band_edges[:-1] * self.band_edges[1:])
        self.band_filters = tuple(
            self._setup_bandpass(f_lo, f_hi, sample_rate)
            for f_lo, f_hi in zip(self.band_edges[:-1], self.band_edges[1:])
        )
        self.envelope_filter = self._setup_lowpass(envelope_lowpass)
        self.band_linear_gains = self._compute_high_freq_tilt(self.band_centers)

    def process(signal):
        """
        Apply the noise-band vocoder to a mono signal.

        Parameters
        ----------
        signal : np.ndarray
            1-D float or integer waveform (mono).

        Returns
        -------
        vocoded: np.ndarray
            Vocoded mono waveform, float64 in normalized to input standard deviation.
        """

        x = signal.astype(float)
        x /= np.max(np.abs(x))

        vocoded = np.zeros_like(x, dtype=float)

        b_lp, a_lp = self.envelope_filter

        for b_bp, a_bp, band_gain in zip(self.band_filters, self.band_linear_gains):
            band_signal = sg.lfilter(b_bp, a_bp, x)

            analytic = sg.hilbert(band_signal)
            envelope = np.abs(analytic)
            envelope = sg.lfilter(b_lp, a_lp, envelope)

            noise = self._rng.standard_normal(len(x))
            noise = sg.lfilter(b_bp, a_bp, noise)
            noise /= np.std(noise)

            vocoded += band_gain * envelope * noise

        vocoded *= np.std(signal) / np.std(vocoded)
        vocoded = vocoded.astype(np.int16)
        return vocoded

    def _compute_high_freq_tilt(self, band_centers):
        """Per-band linear gains for a dB/octave tilt."""
        
        if self.high_freq_tilt == 0
            return np.ones_like(band_centers)

        ref = max(self.min_freq, 1)
        db = self.high_freq_tilt * np.log2(band_centers / ref)
        return 10 ** (db / 20)

    def _setup_bandpass(self, f_lo, f_hi, rate):
        """Butterworth band-pass (b, a) normalized by Nyquist."""
        
        wn = [f_lo / (rate / 2), f_hi / (rate / 2)]
        return sg.butter(self.band_filter_order, wn, btype='band')

    def _setup_lowpass(self, cutoff, rate):
        """Butterworth low-pass (b, a) normalized by Nyquist."""

        wn = cutoff / (rate / 2)
        return sg.butter(self.envelope_filter_order, wn, btype='low')

    @staticmethod
    def _compute_band_edges(n_bands, min_freq, max_freq):
        """Log-spaced band edges from min to max frequency."""

        return np.geomspace(min_freq, max_freq, n_bands + 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Apply a cochlear-implant-style noise-band vocoder to a WAV file.'
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to input WAV file.'
    )
    parser.add_argument(
        'output_file',
        type=str,
        help='Path to output WAV file.'
    )
    args = parser.parse_args()

    sample_rate, input = wav.read(args.input_file)

    voc = NoiseBandVocoder(
        n_bands=12,
        min_freq=200,
        max_freq=8000,
        envelope_lowpass=400,
        high_freq_tilt=2,
        band_filter_order=4,
        envelope_filter_order=2,
        rng_seed=42
    )

    vocoded = voc.process(input)

    wav.write(
        args.output_file,
        voc.sample_rate,
        vocoded
    )
