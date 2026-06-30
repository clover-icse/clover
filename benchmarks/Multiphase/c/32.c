int main(){
    int x, y, z, w;

    // pre-conditions
    y = 0;
    w = 1;
    assume((x == z));
    assume(((z == 0) || (z == 1)));

    // loop body
    while(unknown()){
        if(z == x % 2){
            w = w + y;
        }else{
            w = w - 1;
        }
        z = 1 - z;
        y = y + x -3;
        x = x + 1;
    }

    // post-condition
    if(x > 10){
        assert(w >= 0);
    }
    
}