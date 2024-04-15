import { Component, ElementRef, Input, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import Hls, { HlsConfig } from 'hls.js';
import { VideoService } from './video.service';
import { TuiLoaderModule } from '@taiga-ui/core/components';
// github.com/rightonhana/hls-player

@Component({
	standalone: true,
	selector: 'app-video',
	templateUrl: './video.component.html',
	styleUrls: ['./video.component.less'],
	imports: [
		TuiLoaderModule,
	]
})
export class VideoComponent {
  	loading = true;
	playing = false;
	// private videoEnded = false;
	config:Partial<HlsConfig>  = {
		// "enableWorker": true,
		// "maxBufferLength": 5,
		// "liveBackBufferLength": 1,
		// "liveSyncDuration": 1,
		// "liveMaxLatencyDuration": 1,
		// "liveMaxLatencyDurationCount": 5,
		// "liveDurationInfinity": true,
		// "highBufferWatchdogPeriod": 5,
		"lowLatencyMode": true
	}
	private hls = new Hls();
	private videoListeners = {
		// loadedmetadata: () =>
		// 	this.videoTimeService.setVideoDuration(this.video.nativeElement.duration),
		canplay: () => this.videoService.setLoading(false),
		seeking: () => this.videoService.setLoading(true),
		timeupdate: () => {
			// console.log(this.hls, this.video.nativeElement, this.video.nativeElement.currentTime)
			this.videoService.play()
			setTimeout(() => {
				this.video.nativeElement.play()
				this.playPauseVideo(true);
			  }, 5000);
			// this.video.nativeElement.play()
			if (this.hls.latency > 3){
				this.video.nativeElement.currentTime = this.hls.liveSyncPosition
			}
			// For fix video play status
			if (this.video.nativeElement.currentTime < 65)
				this.video.nativeElement.play();
		},
	};
	
	@Input() videoLink = "http://localhost:888/stream/index.m3u8";
	
	@ViewChild('video', { static: true }) video: any = {} as any;

	constructor(
		private videoService: VideoService,
	) {}

	ngOnInit() {
		
		// http://localhost:888/stream/index.m3u8		  
	}
	ngAfterViewInit(): void {
		//Called after ngAfterContentInit when the component's view has been initialized. Applies to components only.
		//Add 'implements AfterViewInit' to the class.
		this.subscriptions();
		Object.keys(this.videoListeners).forEach((videoListener) => {
			if (this.video) {
				this.video.nativeElement.addEventListener(
					videoListener,
					this.videoListeners[videoListener as keyof typeof this.videoListeners]
				)
			}
		});
	}


	/** Go full screen on double click */
	onDoubleClick() {
		if (document.fullscreenElement) {
			document.exitFullscreen();
		} else {
			const videoPlayerDiv = document.querySelector('.video-player');
			if (videoPlayerDiv?.requestFullscreen) {
				videoPlayerDiv.requestFullscreen();
			}
		}
	}

	/**
	 * Loads the video, if the browser supports HLS then the video use it, else play a video with native support
	 */
	load(currentVideo: string): void {
		if (Hls.isSupported()) {
			this.loadVideoWithHLS(currentVideo);
		} else {
			if (
				this.video.nativeElement.canPlayType('application/vnd.apple.mpegurl')
			) {
				this.loadVideo(currentVideo);
			}
		}
	}

	/**
	 * Play or Pause current video
	 */
	private playPauseVideo(playing: boolean) {
		this.playing = playing;
		this.video.nativeElement[playing ? 'play' : 'pause'];
	}

	/**
	 * Setup subscriptions
	 */
	private subscriptions() {
		this.videoService.playingState$.subscribe((playing) =>
			this.playPauseVideo(playing)
		);
    	this.load(this.videoLink)
		this.videoService.loading$.subscribe((loading) => (this.loading = loading));
		// this.playPauseVideo(true)
	}

	/**
	 * Method that loads the video with HLS support 
	 */
	private loadVideoWithHLS(currentVideo: string) {
		this.hls.loadSource(currentVideo);
		this.hls.attachMedia(this.video.nativeElement);
		this.playPauseVideo(true);
		// this.hls.on(Hls.Events.MANIFEST_PARSED, () => this.playPauseVideo(true)); //  this.video.nativeElement.play()
	}

	/**
	 * Method that loads the video without HLS support
	 */
	private loadVideo(currentVideo: string) {
		this.video.nativeElement.src = currentVideo;
	}
}
