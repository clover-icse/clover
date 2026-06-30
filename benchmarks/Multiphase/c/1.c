int main(){
    int x;
    int y;

    //pre-condition
    x = 0;
    y = 5000;

    //loop-body
    while(unknown()){
        if(x >= 5000){
            y = y + 1;
        }
        x = x + 1;
    }

    //post-condition
    if(x == 10000){
        assert(y == x);
    }
    
}